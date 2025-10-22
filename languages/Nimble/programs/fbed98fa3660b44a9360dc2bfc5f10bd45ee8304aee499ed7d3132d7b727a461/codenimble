import std/[os, strutils]

proc init*(dir: string): void =
  createDir dir
  writeFile(dir / "nimble.toml", "[package]
name = "."
version = "0.1.0"
author = "Your Name <your.email@example.com>"
description = "A short description"
skipUserQuery = true
skipBuildDependencies = true
requires = {"nim >= 1.4"}
[dependencies]
[dependencies.test]
[tasks.build]
[tasks.test]")
  echo "Initialized Nimble package in: $1" % dir