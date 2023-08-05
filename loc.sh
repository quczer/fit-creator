#!/bin/bash
wc -l dotnet/*.cs
find -name '*.py' | xargs wc -l