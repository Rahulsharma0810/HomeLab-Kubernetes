# Talosctl setup and upgrade runbook (Essentials)

Files in this repo
- `talosconfig`: Talos client config (endpoints/nodes)
- `kubeconfig`: Kubernetes client config

Prereqs
- Network access to nodes on TCP 50000 (Talos API)
- kubectl access to 6443
- talosctl installed (matching major/minor preferred)

Quick checks
- `talosctl --talosconfig talosconfig config info`
- `talosctl --talosconfig talosconfig -n <controlPlaneIP> version`
- `talosctl --talosconfig talosconfig -n <controlPlaneIP> health`
  - Note: Health must target a control-plane node; running against a worker returns “kubeconfig is only available on control plane nodes”.

Example talosconfig (minimal)
```
endpoints:
  - 192.168.0.5
nodes:
  - 192.168.0.5
  - 192.168.0.6
```

Node maintenance
- Cordon/drain (preferred):
  - `kubectl --kubeconfig kubeconfig cordon <nodeName>`
  - `kubectl --kubeconfig kubeconfig drain <nodeName> --ignore-daemonsets --delete-emptydir-data --grace-period=30 --timeout=10m`
  - If PDBs block drain and you accept disruption:
    - `kubectl --kubeconfig kubeconfig drain <nodeName> --ignore-daemonsets --delete-emptydir-data --grace-period=30 --timeout=10m --disable-eviction`
- Uncordon:
  - `kubectl --kubeconfig kubeconfig uncordon <nodeName>`

Talos upgrade (in-place)
- Check current version:
  - `talosctl --talosconfig talosconfig -n <nodeIP> version`
- Upgrade a node to v1.11.1:
  - `talosctl --talosconfig talosconfig upgrade --nodes <nodeIP> --image ghcr.io/siderolabs/installer:v1.11.1 --timeout=30m`
- Verify after reboot:
  - `talosctl --talosconfig talosconfig -n <nodeIP> version`
  - `talosctl --talosconfig talosconfig -n <controlPlaneIP> health`

Cluster health
- Full health via control-plane:
  - `talosctl --talosconfig talosconfig -n <controlPlaneIP> health`
- Kubernetes nodes:
  - `kubectl --kubeconfig kubeconfig get nodes -o wide`

Notes
- Single control-plane clusters will temporarily lose the API during control-plane upgrades.
- Prefer upgrading workers first, then control-plane.
- If health waits too long:
  - `talosctl --talosconfig talosconfig -n <controlPlaneIP> health --wait-timeout=20m`
