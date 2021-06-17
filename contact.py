'''Circular convolution algorithm to get contact between two surfaces
Author: Saad Ahmed Khan
Email: s.aad@live.com

Constraints: 
1. Within the threshold range each node on one surface has only one closest node on the other surface.
See tests below, case 3 voilates this assumption. This can cause error in result if the threshold is around the edges
where the two contacting surfaces are moving away from each other but the sample size can be used to control this error
by not selecting a very large number such that edge node are included while calculating the threshold
2. Rounding off threshold and least distance values to 5 decimal places to avoid computational precision
error
'''

# numerical python library comes with blender
import numpy as np
# blender python API
import bpy
C = bpy.context

''' @param samplesize - set by user to calculate threshold for contacting nodes.
e.g 7000 will select 7000 pair of nodes which are least distant in the two selected
objects
@param selected_objects - two objects selected by the user where there needs to be 
a contact
'''
samplesize = 3
selected_objects = C.selected_objects

def separateCoordinates(obj):
    ''' returns a list of tuples with object's vertex's coordinates and respective index
    '''
    return [(obj.matrix_world * v.co, v.index) for v in obj.data.vertices]

def addToGroup(obj, vertices):
    ''' add vertices to object 
    @param obj - object to which vertices will be added
    @param vertices - vertices to be added
    '''
    obj.vertex_groups.new(name='contact').add(vertices, 1.0, 'ADD')

def main(samplesize_ = samplesize, selected_objects_ = selected_objects):
    ''' main driver function for generating contact
    References 
    Euclidean Distance - https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
    Third Party Modules - https://blender.stackexchange.com/questions/5287/using-3rd-party-python-modules
    Minimum Euclidean Distance - https://stackoverflow.com/questions/1871536/minimum-euclidean-distance-between-points-in-two-different-numpy-arrays-not-wit
    '''

    if(len(selected_objects_) != 2):
        raise Exception('Try again after selecting two objects in object mode')

    # assuming first seleted is larger that is, has more vertices then the second
    large_obj, small_obj = selected_objects_[0], selected_objects_[1]
    separated1 = separateCoordinates(large_obj)
    separated2 = separateCoordinates(small_obj)
    large_co, large_v = zip(*separated1)
    small_co, small_v = zip(*separated2)

    # checking assumption
    diff = len(separated1) - len(separated2)
    if diff < 0:
        large_obj, small_obj = small_obj, large_obj
        large_co, small_co = small_co, large_co
        large_v, small_v = small_v, large_v

    # converting coordinates to numpy array
    small_co = np.array(small_co)
    large_co = np.array(large_co)

    # no of iterations required to calculate distance between all points in small and large coordinates array
    absdiff = abs(diff)
    iterations = len(small_co) + absdiff - 1

    # rolling pointer for circular convolution. it will roll large objects coordinates array at each iteration. 
    # all items will be pushed to the next index and the last item will be pushed to first
    rolling_pointer = np.arange(len(large_co))
    # dynamic pointer for sorting by small object's coordinates array such that coordinates at the same index are the closest
    # pair nodes
    dynamic_pointer = np.copy(rolling_pointer)

    # limit for resizing large coordinates array equal to small coordinates array
    limit = len(large_co) - absdiff

    # initial iteration
    rolling_pointer_resized = rolling_pointer[:limit]
    large_co_resized = large_co[rolling_pointer_resized]

    # np.linalg.norm - applying distance formula
    leastdists = np.linalg.norm(small_co - large_co_resized, axis=1)

    for i in range(iterations):
        # rolling indexes for circular convolution
        rolling_pointer = np.roll(rolling_pointer, -1)

        # next iteration
        rolling_pointer_resized = rolling_pointer[:limit]
        large_co_resized = large_co[rolling_pointer_resized]
        new = np.linalg.norm(small_co - large_co_resized, axis=1)

        # perpare mask where new least distances are found
        mask = new < leastdists
        # check if new distances are found
        if np.any(mask):
            # update dynamic pointer where new least distances are found
            dynamic_pointer[:limit][mask] = rolling_pointer_resized[mask]
            # update distance with new least distances
            leastdists[mask] = new[mask]    

    threshold = np.amax(np.sort(leastdists)[:samplesize_])
    
    # rounding to avoid precision error
    threshold = round(threshold, 5)
    leastdists = [round(dist, 5) for dist in leastdists]
    
    # prepare mask for least distances which qualify as contancting nodes
    mask = leastdists <= threshold
    
    # converting vertices indexes for numpy operations
    large_v_np = np.array(large_v)
    small_v_np = np.array(small_v)

    # dynamic pointer sorted by small object's coordinates array such that coordinates at the same index are the closest
    # pair nodes
    dynamic_pointer_sorted = dynamic_pointer[:limit][mask]
    
    # slicing into vertices pairs
    large_v_np = large_v_np[dynamic_pointer_sorted]
    small_v_np = small_v_np[mask]

    # converting to list
    large_v_list = large_v_np.tolist()
    small_v_list = small_v_np.tolist()
    
    if(not len(large_v_list) == len(small_v_list)):
        raise Exception('Equal number of nodes not found contact developer')

    # adding to groups
    addToGroup(large_obj, large_v_list)
    addToGroup(small_obj, small_v_list)

    if(TESTING):
        # slicing into coordinates pairs
        small_co = small_co[mask]
        large_co = large_co[dynamic_pointer_sorted]
        dists = np.linalg.norm(small_co - large_co, axis=1)
        return {
            "length" : len(large_v_list),
            "threshold" : threshold,
            "dists" : [round(dist, 5) for dist in dists]
        }

TESTING = False

def evaluate(computed, expected):
    print("evaluation")
    print("computed:")
    print(computed)
    print("expected:")
    print(expected)
    print(computed['length'] == expected['length'])
    print(computed['threshold'] == expected['threshold'])
    print(computed['dists'] == expected['dists'])

if not TESTING:
    main()
elif TESTING:
    C.area.type = 'VIEW_3D'
    bpy.ops.view3d.snap_cursor_to_center()

    bpy.ops.mesh.primitive_cube_add()
    ncube1 = C.active_object.name    

    bpy.ops.mesh.primitive_cube_add()
    ncube2 = C.active_object.name

    cube1 = bpy.data.objects[ncube1]
    cube2 = bpy.data.objects[ncube2]

    # case 1
    samplesize = 1
    cube2.location[2] = 3
    C.scene.update()


    expected = {
        "length" : 4,
        "threshold" : 1,
        "dists" : [1,1,1,1]
    }
    computed = main(samplesize, [cube1, cube2])
    evaluate(computed, expected)
    
    # case 2
    cube2.location[1] = 3
    C.scene.update()
    expected_threshold = round(2**(1/2), 5)
    expected = {
        "length" : 2,
        "threshold" : expected_threshold,
        "dists" : [expected_threshold for i in range(2)]
    }
    computed = main(samplesize, [cube1, cube2])
    evaluate(computed, expected)

    # case 3 - this will fail because it voilates the assumption mentioned at the begining of this file
    samplesize = 3
    # expected_threshold - in case code was developed to cater for the assumption
    expected_threshold = round((3**2 + 3**2)**(1/2), 5)
    expected = {
        "length" : 6,
        "threshold" : expected_threshold,
        "dists" : [expected_threshold for i in range(6)]
    }
    computed = main(samplesize, [cube1, cube2])
    evaluate(computed, expected)
    
    C.area.type = 'TEXT_EDITOR'

def adjust_precision(v):
    pass