# pycrust
PyCRUST : Python Cosmic Rays Underground Simulation Tool

Jupyter based Docker container system for running GEANT4 in a web browser for cosmic ray studies.

The command below can be used to run the server.
```
docker run --rm -it -v $PWD:/data/mnt -p 8168:8168 -t johnpatrickstowell/pycrust:examples

[I 2024-11-16 00:00:47.902 ServerApp] notebook_shim | extension was successfully linked.
[I 2024-11-16 00:00:47.984 ServerApp] notebook_shim | extension was successfully loaded.
[I 2024-11-16 00:00:47.987 ServerApp] jupyter_lsp | extension was successfully loaded.
[I 2024-11-16 00:00:47.991 ServerApp] jupyter_server_terminals | extension was successfully loaded.
[I 2024-11-16 00:00:47.993 LabApp] JupyterLab extension loaded from /usr/local/lib/python3.9/site-packages/jupyterlab
[I 2024-11-16 00:00:47.993 LabApp] JupyterLab application directory is /usr/local/share/jupyter/lab
[I 2024-11-16 00:00:47.994 LabApp] Extension Manager is 'pypi'.
[I 2024-11-16 00:00:48.054 ServerApp] jupyterlab | extension was successfully loaded.
[I 2024-11-16 00:00:48.055 ServerApp] Serving notebooks from local directory: /data
[I 2024-11-16 00:00:48.056 ServerApp] Jupyter Server 2.14.2 is running at:
[I 2024-11-16 00:00:48.056 ServerApp] http://8bc4cf3d8ef7:8168/lab?token=d1996c339d9ec59f8099440f8aabd54ef60ed7027497effb
[I 2024-11-16 00:00:48.056 ServerApp]     http://127.0.0.1:8168/lab?token=d1996c339d9ec59f8099440f8aabd54ef60ed7027497effb
[I 2024-11-16 00:00:48.056 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 2024-11-16 00:00:48.061 ServerApp] No web browser found: Error('could not locate runnable browser').
[C 2024-11-16 00:00:48.061 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/g4user/.local/share/jupyter/runtime/jpserver-7-open.html
    Or copy and paste one of these URLs:
        http://8bc4cf3d8ef7:8168/lab?token=d1996c339d9ec59f8099440f8aabd54ef60ed7027497effb
        http://127.0.0.1:8168/lab?token=d1996c339d9ec59f8099440f8aabd54ef60ed7027497effb

```

To access the server once you get this message you need to follow the URL given
```
http://8bc4cf3d8ef7:8168/lab?token=d1996c339d9ec59f8099440f8aabd54ef60ed7027497effb
```



### Running on windows.
```
docker run --rm -it -v ./:/data/mnt -p 8168:8168 -t johnpatrickstowell/pycrust:examples
```