"""TF-IDF + Logistic Regression phishing detection training and held-out evaluation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline

from ..config import settings
from .dataset import DATASET


def build_pipeline() -> Pipeline:
    """Combines word n-grams and character n-grams for robust scam/URL token detection."""
    features = FeatureUnion(
        transformer_list=[
            (
                "word_tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    max_features=4500,
                    sublinear_tf=True,
                    strip_accents="unicode",
                ),
            ),
            (
                "char_tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    max_features=4500,
                    sublinear_tf=True,
                ),
            ),
        ]
    )
    classifier = LogisticRegression(
        C=2.0,
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )
    return Pipeline([("features", features), ("clf", classifier)])


def train_and_evaluate(force: bool = False) -> Tuple[Pipeline, Dict[str, Any]]:
    """Train on 75% stratified split, evaluate on 25% held-out test set, then save artifact."""
    model_path: Path = settings.model_artifact_path
    metrics_path: Path = settings.model_metrics_path

    if not force and model_path.exists() and metrics_path.exists():
        pipeline = joblib.load(model_path)
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        return pipeline, metrics

    texts = [sample.text for sample in DATASET]
    labels = np.array([sample.label for sample in DATASET], dtype=int)

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    eval_pipeline = build_pipeline()
    eval_pipeline.fit(X_train, y_train)

    y_pred = eval_pipeline.predict(X_test)
    y_prob = eval_pipeline.predict_proba(X_test)[:, 1]

    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    tn, fp, fn, tp = [int(v) for v in cm.ravel()]

    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    accuracy = float(accuracy_score(y_test, y_pred))
    roc_auc = float(roc_auc_score(y_test, y_prob))

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_f1 = cross_val_score(build_pipeline(), texts, labels, cv=cv, scoring="f1")

    # Fit production pipeline on full curated dataset after recording honest held-out metrics
    prod_pipeline = build_pipeline()
    prod_pipeline.fit(texts, labels)

    # Extract top predictive word features for explainability transparency
    word_vec: TfidfVectorizer = prod_pipeline.named_steps["features"].transformer_list[0][1]
    clf: LogisticRegression = prod_pipeline.named_steps["clf"]
    word_feature_count = len(word_vec.get_feature_names_out())
    word_names = word_vec.get_feature_names_out()
    word_coefs = clf.coef_[0][:word_feature_count]
    top_phishing_idx = np.argsort(word_coefs)[-12:][::-1]
    top_benign_idx = np.argsort(word_coefs)[:10]

    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    metrics: Dict[str, Any] = {
        "model_name": "TF-IDF (Word + Char N-grams) + Logistic Regression",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "total_samples": len(DATASET),
            "phishing_samples": int(np.sum(labels == 1)),
            "benign_samples": int(np.sum(labels == 0)),
            "train_size": len(X_train),
            "held_out_test_size": len(X_test),
            "split_strategy": "75% / 25% stratified train/held-out test split (random_state=42)",
            "channels": sorted({s.channel for s in DATASET}),
            "description": (
                "Curated SME-focused phishing & legitimate communication corpus covering Email, SMS, "
                "and WhatsApp across banking/KYC lures, UPI PIN scams, GST/tax impersonation, "
                "courier scams, BEC invoice fraud, credential harvesting, and hard-negative benign alerts."
            ),
        },
        "held_out_metrics": {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "confusion_matrix": {
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp,
                "matrix": [[tn, fp], [fn, tp]],
                "labels": ["Legitimate (0)", "Phishing (1)"],
            },
            "per_class": {
                "legitimate": {
                    "precision": round(float(report_dict["0"]["precision"]), 4),
                    "recall": round(float(report_dict["0"]["recall"]), 4),
                    "f1": round(float(report_dict["0"]["f1-score"]), 4),
                    "support": int(report_dict["0"]["support"]),
                },
                "phishing": {
                    "precision": round(float(report_dict["1"]["precision"]), 4),
                    "recall": round(float(report_dict["1"]["recall"]), 4),
                    "f1": round(float(report_dict["1"]["f1-score"]), 4),
                    "support": int(report_dict["1"]["support"]),
                },
            },
        },
        "cross_validation_5fold": {
            "mean_f1": round(float(np.mean(cv_f1)), 4),
            "std_f1": round(float(np.std(cv_f1)), 4),
            "fold_scores": [round(float(x), 4) for x in cv_f1],
        },
        "top_indicators": {
            "phishing_terms": [
                {"term": str(word_names[i]), "weight": round(float(word_coefs[i]), 3)}
                for i in top_phishing_idx
            ],
            "legitimate_terms": [
                {"term": str(word_names[i]), "weight": round(float(word_coefs[i]), 3)}
                for i in top_benign_idx
            ],
        },
        "limitations": [
            "Trained on a curated SME corpus rather than live enterprise mail telemetry; novel zero-day templates or non-English scripts outside training patterns may score lower.",
            "Short, ambiguous messages (< 15 words) have lower statistical confidence and rely more heavily on transparent heuristic verification.",
            "Risk bands (0-24 Low, 25-49 Moderate, 50-74 High, 75-100 Critical) are CyberShield AI application thresholds, not universal industry standards.",
        ],
    }

    joblib.dump(prod_pipeline, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return prod_pipeline, metrics


def get_model_and_metrics() -> Tuple[Pipeline, Dict[str, Any]]:
    return train_and_evaluate(force=False)

