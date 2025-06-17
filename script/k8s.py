import os
import subprocess

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

kubectl_command = "kubectl get namespaces -o jsonpath='{.items[*].metadata.name}'"
namespaces = subprocess.check_output(kubectl_command, shell=True, text=True).split()

resources = ["configmap", "secret", "deployment", "ingress", "pvc", "service", "serviceaccount"]

for namespace in namespaces:
    print(f"Namespace: {namespace}")

    ns_dir = namespace
    create_directory(ns_dir)

    for resource in resources:
        resource_dir = os.path.join(ns_dir, resource)
        create_directory(resource_dir)

        kubectl_command = f"kubectl get {resource} -n {namespace} -o custom-columns=NAME:.metadata.name --no-headers"
        resources_list = subprocess.check_output(kubectl_command, shell=True, text=True).split()

        for res in resources_list:
            kubectl_command = f"kubectl get {resource} {res} -n {namespace} -o yaml"
            resource_yaml = subprocess.check_output(kubectl_command, shell=True, text=True)
            with open(os.path.join(resource_dir, f"{res}.yaml"), "w") as yaml_file:
                yaml_file.write(resource_yaml)

        printe(f"Exported manifests for {namespace}")
