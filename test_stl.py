from stl_models import STL


class TestStl:
    def test_parse_stl(self):
        stl = STL("models/cube.stl")

        assert len(stl.triangles) == 12
        assert len(stl.vertices) == 8
        assert len(stl.edges) == 18
