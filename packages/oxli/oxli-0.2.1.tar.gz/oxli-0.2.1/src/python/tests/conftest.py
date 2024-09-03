@pytest.fixture(params=[True, False])
def default_is_False(request):
    return request.param
