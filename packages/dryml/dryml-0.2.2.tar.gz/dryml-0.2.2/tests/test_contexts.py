import dryml


def test_resource_pool_1():
    pool_obj = dryml.context.ResourcePool(num_cpus=3, num_gpus=3, _test=True)

    req = dryml.context.ResourceRequest(num_gpus=1)
    alloc = pool_obj.request(req)

    assert alloc.satisfies(req)

    pool_obj.release(alloc)

    req2 = dryml.context.ResourceRequest({'gpu/1': 0.5})
    alloc = pool_obj.request(req2)

    alloc2 = pool_obj.request(req2)

    assert alloc.satisfies(req2)
    assert alloc2.satisfies(req2)

    pool_obj.release(alloc)
    pool_obj.release(alloc2)

    for key in pool_obj.resource_map:
        assert pool_obj.resource_map[key] == 1.


def test_context_check_1():
    with dryml.context.ContextManager(
            resource_requests={'default': {'num_cpus': 1}}):
        dryml.context.context_check({'default': {}})


def test_context_check_2():
    with dryml.context.ContextManager(
            resource_requests={'default': {'num_cpus': 1}}):
        try:
            dryml.context.context_check({'tf': {}})
            assert False
        except dryml.context.ContextIncompatibilityError:
            pass
