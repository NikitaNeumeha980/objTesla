smesh = smeshBuilder.New()
print("Creating Parallel Mesh")
par_mesh = smesh.ParallelMesh(rubik_cube, name="par_mesh")

print("Creating hypoehtesis for netgen")
NETGEN_3D_Parameters_1 = smesh.CreateHypothesisByAverageLength( 'NETGEN_Parameters',
                                         'NETGENEngine', 34.641, 0 )
print("Adding hypothesis")
par_mesh.AddGlobalHypothesis(NETGEN_3D_Parameters_1)

print("Setting parallelism method")
par_mesh.SetParallelismMethod(smeshBuilder.MULTITHREAD)

print("Setting parallelism options")
param = par_mesh.GetParallelismSettings()
param.SetNbThreads(6)

print("Starting parallel compute")
is_done = par_mesh.Compute()
if not is_done:
    raise Exception("Error when computing Mesh")

print("  Tetrahedron: ",  par_mesh.NbTetras())
print("  Triangle: ", par_mesh.NbTriangles())
print("  edge: ", par_mesh.NbEdges())

assert  par_mesh.NbTetras() > 0
assert  par_mesh.NbTriangles() > 0
assert  par_mesh.NbEdges() > 0
