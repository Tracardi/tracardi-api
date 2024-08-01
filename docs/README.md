# Install
```
pip install -r docs/requirements.txt 
```


# Test
run in tracardi-api/docs
```
docker run --rm -it -p 8100:8000 -v ${PWD}:/docs squidfunk/mkdocs-material:9.5.1
```

# Build
Type `mkdocs build` in folder / in tracardi-api (it must be single project, without attached tracardi, etc.)