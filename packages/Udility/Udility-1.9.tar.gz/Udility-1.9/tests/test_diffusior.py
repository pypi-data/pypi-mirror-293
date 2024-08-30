import unittest
from Udility.diffusior import generate_image_from_text, get_detailed_instructions, generate_svg_from_instructions, svg_to_png

class TestDiffusior(unittest.TestCase):
    def test_get_detailed_instructions(self):
        instructions = get_detailed_instructions("Lifecycle of amoeba.")
        self.assertIsInstance(instructions, str)
        self.assertGreater(len(instructions), 0)

    def test_generate_svg_from_instructions(self):
        svg_code = generate_svg_from_instructions("Draw a circle.")
        self.assertIsInstance(svg_code, str)
        self.assertTrue(svg_code.startswith("<svg>") and svg_code.endswith("</svg>"))

    def test_svg_to_png(self):
        svg_code = "<svg height='100' width='100'><circle cx='50' cy='50' r='40' stroke='black' stroke-width='3' fill='red' /></svg>"
        svg_to_png(svg_code, "test_output.png")
        self.assertTrue(os.path.exists("test_output.png"))

if __name__ == "__main__":
    unittest.main()
