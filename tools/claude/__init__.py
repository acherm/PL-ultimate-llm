# tools/claude - Claude Code Agent System
#
# This module provides an independent system for using Claude Code CLI agents
# to contribute programming languages to the collection.
#
# Components:
#   - turn.py: Single agent turn on a dedicated branch
#   - orchestrator.py: Parallel batch runner with model rotation
#   - merge.py: Branch merge coordinator with duplicate detection
#   - prompt.py: Agent prompt templates
#   - config.yaml: Configuration settings

__version__ = "0.1.0"
