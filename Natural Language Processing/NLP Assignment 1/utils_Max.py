
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, f1_score, log_loss

def evaluate_model(model, X_test, y_true):
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_proba)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    logloss = log_loss(y_true, y_proba)
    return acc, roc_auc, prec, rec, f1, logloss
