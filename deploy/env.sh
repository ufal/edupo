# Central path configuration for the EduPo systemd launcher scripts.
# Sourced by start-*.sh. Adjust to match the server, nothing else needs editing.

# Repo checkout on the server
REPO=/home/jarda/edupo

# bin directory of the Python environment with the backend + model dependencies
# (find it on the server with:  conda activate edupo; dirname "$(which python3)")
PYBIN=/home/jarda/miniconda3/envs/edupo/bin
