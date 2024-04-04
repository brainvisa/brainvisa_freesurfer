# -*- coding: utf-8 -*-

import time
from numpy import *
import numpy
import pickle
from soma import aims, aimsalgo


def remeshAims(unstructured, target):
    # ensure the target mesh has a radius of 100.
    r = sum([p.norm() for p in target.vertex()]) / len(target.vertex())
    r = 100. / r
    for p in target.vertex():
        p *= r
    mi = aims.MeshInterpoler(unstructured, target)
    mi.project()
    t = mi.projectedTriangles()
    tc1, tc2 = mi.projectedTriCoord1(), mi.projectedTriCoord2()
    isiN = numpy.array(t[0].np)
    c1 = numpy.array(tc1[0].np)
    c2 = numpy.array(tc2[0].np)
    isin = numpy.hstack((numpy.reshape(c1, [len(c1), 1]),
                         numpy.reshape(c2, [len(c2), 1])))
    return isiN, isin


def remesh(unstructured, target):
    T = time.time()
    # svertex = target.getArraysFromIntent(GiftiIntentCode.NIFTI_INTENT_POINTSET)[0].data
    # uvertex = unstructured.getArraysFromIntent(GiftiIntentCode.NIFTI_INTENT_POINTSET)[0].data
    # ufaces =
    # unstructured.getArraysFromIntent(GiftiIntentCode.NIFTI_INTENT_TRIANGLE)[0].data
    svertex = array(target.vertex())
    uvertex = array(unstructured.vertex())
    ufaces = array(unstructured.polygon())
    # roughly same center and same bounding box
    if (not allclose(svertex.mean(0), uvertex.mean(0), atol=1e-2)) or (not allclose(svertex.max(0), uvertex.max(0), atol=1e-2)):
        print("\nWARNING : different mean or max(0)\n")
    polycenters = uvertex[ufaces].mean(1)
    maxs = sum((uvertex[ufaces] - polycenters[:, newaxis, :])**2, 2).max(1)
    # precompute some stuffs
    dmax = sqrt(maxs.max())
    smin, smax = svertex.min(0) - 2 * dmax, svertex.max(0) + 2 * dmax
    grid_xyz = [r_[smin[i]:smax[i]:dmax] for i in (0, 1, 2)]
    S = [searchsorted(g, s) for g, s in zip((grid_xyz), svertex.T)]
    d = [[set() for _ in grid_xyz[0]] for x in (0, 1, 2)]  # parcel list
    for dxyz, Sxyz in zip(d, S):
        for v, n in enumerate(Sxyz):
            dxyz[n - 1].add(v)
            dxyz[n].add(v)
            dxyz[n + 1].add(v)
    # the isinN and isin lists will eventually, for each of the structured mesh
    # vertex, store the associated unstructured triangle index, and the 3
    # weights
    isinN, isin = [-1] * len(svertex), [(-1, -1)] * len(svertex)
    # will iterate on the unstructured-mesh triangles (their centers, actually)
    triangle = empty((3, 3))
    a, bc = triangle[0], triangle[1:]  # setup some views
    print(time.time() - T)
    for i, p in enumerate(polycenters):
        if i % 30000 == 0:
            print(i, "/", len(polycenters))
        # find closest points of p : first a rough filter, then an exact filter
        binxyz = [searchsorted(grid_xyz[x], p[x])
                  for x in (0, 1, 2)]  # le bin de p
        W = d[0][binxyz[0]].intersection(
            d[1][binxyz[1]]).intersection(d[2][binxyz[2]])
        W = fromiter(W, int, len(W))
        W = W[sum((svertex[W] - p)**2, 1) <= maxs[i]]
        if len(W) == 0:
            continue
        triangle[:] = uvertex[ufaces[i]]
        bc -= a
        proj = inner(bc, bc)
        # (precompute part of the weight computation for the current triangle)
        m00, m01, m11 = float(proj[0, 0]), float(proj[0, 1]), float(proj[1, 1])
        detA = m00 * m11 - m01 * m01
        m00 /= detA
        m01 /= detA
        m11 /= detA
        # For each (triangle-edges projected) candidate vertex of the structured mesh,
        # computes the 3 weights, and store the results if it belongs to the
        # triangle.
        for v0v1, n in zip(dot(svertex[W] - a, bc.T), W):
            v0, v1 = float(v0v1[0]), float(v0v1[1])
            lam, gam = m11 * v0 - m01 * v1, -m01 * v0 + m00 * v1
            if (lam >= -0.001) & (gam >= -0.001) & (lam + gam <= 1.001):
                isinN[n] = i
                isin[n] = lam, gam
            elif isinN[n] < 0:  # debug
                isinN[n] -= 1
                isin[n] = lam, gam
    print(time.time() - T)
    return isinN, isin

# def apply_remesh(remesh_params, orig_mesh, orig_pal):
#	isinN, isinT = remesh_params[0], transpose(remesh_params[1])
#	if -1 in isinN:
#		print("\nWARNING : -1 in remeshing output\n")
#	ufaces = orig_mesh.getArraysFromIntent(GiftiIntentCode.NIFTI_INTENT_TRIANGLE)[0].data
#	T = rollaxis(orig_pal[ufaces[isinN]], 0, 3)
#	texout = ((1 - isinT[0] - isinT[1]) * T[0] + isinT[0] * T[1] + isinT[1] * T[2]).T
#	return texout.astype(orig_pal.dtype)
#
# plus lente, mais bouffe moins de ram
# def apply_remesh_slower(remesh_params, orig_mesh, orig_pal):
#	isinN, isin = remesh_params[0], array(remesh_params[1])
#	assert(not -1 in isinN)
#	ufaces = orig_mesh.getArraysFromIntent(GiftiIntentCode.NIFTI_INTENT_TRIANGLE)[0].data
#	texout = zeros((len(isinN), len(orig_pal[0])), orig_pal.dtype)
#	for n in range(len(isin)):
#		t = orig_pal[ufaces[isinN[n]]]
#		value = (1-isin[n][0]-isin[n][1])*t[0] + isin[n][0]*t[1] + isin[n][1]*t[2]
#		texout[n] = value
#	return texout

# if __name__ == '__main__':
#	if len(sys.argv) == 5:
#		srcmesh, srcpal, dstmesh, dstpal = sys.argv[1:]
#		assert(srcmesh.endswith('.gii') and dstmesh.endswith('.gii'))
#		assert(srcpal.endswith('.npy') and dstpal.endswith('.npy'))
#		srcgii = gifti.loadImage(srcmesh)
#		dstgii = gifti.loadImage(dstmesh)
#		for x in srcgii, dstgii:
#			x.showSummary()
#		print("computing transformation")
#		remesh_params = remesh(srcgii, dstgii)
#		print("applying on palettes")
#		texout = apply_remesh(remesh_params, srcgii, numpy.load(srcpal))
#		numpy.save(open(dstpal, 'w'), texout)
#	elif len(sys.argv) == 4:
#		srcmesh, dstmesh, isinFile = sys.argv[1:]
#		print('srcmesh', srcmesh)
#		print('dstmesh', dstmesh)
#		print('isinFile', isinFile)
#		assert(srcmesh.endswith('.gii') and dstmesh.endswith('.gii'))
#		srcgii = gifti.loadImage(srcmesh)
#		dstgii = gifti.loadImage(dstmesh)
#		for x in srcgii, dstgii:
#			x.showSummary()
#		print("computing transformation")
#		remesh_params = remesh(srcgii, dstgii)
#		f = open(isinFile,'w')
#		pickle.dump(remesh_params, f)
#		f.close()
#	elif 1:
# auto test (sans args)
#		mesh = gifti.loadImage("uvlarge.gii")
#		sphere = gifti.loadImage("icolarge.gii")
#		print(mesh.showSummary())
#		print(sphere.showSummary())
# same center
#		print(allclose(mesh.arrays[0].data.mean(0), sphere.arrays[0].data.mean(0), atol=1e-4))
# same bounding box
#		print(allclose(mesh.arrays[0].data.max(0), sphere.arrays[0].data.max(0), atol=1e-2))
#		isinN, isin = remesh(mesh, sphere)
#		isin_correct = load("isincorrect.npy")
#		print(allclose(column_stack([isinN, isin]), isin_correct))
#

# Brainvisa function


def regularizeSphericalMesh(srcmesh, isinFile, dstmesh='./ico100_7.mesh'):
    print("source", srcmesh)
    print("isin", isinFile)
    print("destination", dstmesh)
    srcgii = aims.read(srcmesh)
    dstgii = aims.read(dstmesh)
    print("computing transformation")
    # remesh_params = remesh(srcgii, dstgii)
    remesh_params = remeshAims(srcgii, dstgii)
    f = open(isinFile, 'wb')
    pickle.dump(remesh_params, f)
    f.close()
