Steps for Kyverno Deployment

# Install Kyverno (idempotent — skips if already installed)
helm repo add kyverno https://kyverno.github.io/kyverno/ --force-update

# Wait for Kyverno admission controller to be ready before applying policies
helm upgrade --install kyverno kyverno/kyverno -n kyverno --create-namespace --wait --timeout 120s


# 1. Create a GCP service account for Kyverno
gcloud iam service-accounts create kyverno-sa \
  --display-name="Kyverno Admission Controller"

# 2. Grant it Artifact Registry reader
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:kyverno-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"

# 3. Bind the K8s SA to the GCP SA via Workload Identity
gcloud iam service-accounts add-iam-policy-binding \
  kyverno-sa@${PROJECT_ID}.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:${PROJECT_ID}.svc.id.goog[kyverno/kyverno-admission-controller]"

# 4. Annotate the K8s ServiceAccount
kubectl annotate sa kyverno-admission-controller -n kyverno \
  iam.gke.io/gcp-service-account=kyverno-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com \

  --overwrite
# 5. Restart Kyverno to pick up the new identity
kubectl rollout restart deployment kyverno-admission-controller -n kyverno
kubectl rollout status deployment kyverno-admission-controller -n kyverno --timeout=120s