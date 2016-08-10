import unittest
from hiring import submission

class TestCommentMethods(unittest.TestCase):
    def test_terms(self):
        c = submission.Comment({
            'text' : """
            Smartcar | Backend Engineer | SF & Mountain View | Onsite
            I'm an early employee at Smartcar. When I was job hunting back in the October, I looked at early stage startups in interesting spaces like eSports, VR, insurance, automotive etc. Smartcar is an automotive-related startup that's building the developer platform for the connected car.
            Smartcar is in a massive space (auto-related industry is 10% of US GDP), has a great team, is well funded with an amazing investor, we're making money and tons of other great early traction.
            We're looking to hire 3 engineers ASAP. Your voice will be heard and you will determine the company's technical roadmap.
            You should be a generalist who will be tasked with designing a modern API platform for cars, building secure web and API backends, integrating with testing, coverage and deployment pipelines and more. Our stack is Node.js, Postgres, Redis, Docker, AWS.
            $95K to $130K + up to 1.0% equity
            """
        })

        self.assertIn('node.js', c.terms())
        self.assertIn('AWS', c.terms())
        self.assertIn('api', c.terms())
        self.assertNotIn('secure', c.terms())

        c = submission.Comment({
        'text' : """
        Peloton Technology | Mountain View, CA. | ONSITE | Full-time
        Work on Autonomous Vehicle Technology. It's happening now. Check us out at www.peloton-tech.com and email sandra@peloton-tech.com if you know you are good.
        We've 5+ openings: 1) Vehicle Software Engineer - expert C++ 2) Vehicle Software Engineer - Go 3) Build & Release Engineer - Commercial App Dev. Learn Bazel 4) Firmware Engineer - RTOS 5) Embedded Electrical Engineer - Circuit Design / PCB
        WHAT WE DO: At Peloton Technology, we are transforming the trucking industry, bringing groundbreaking safety, efficiency and data to the trucks that drive the economy. WHAT? In short, we're mastering Truck platooning technology and it works!
        FOUNDERS: Peloton's founders are Stanford University alumni with roots in Stanford's autonomous vehicle program, Volkswagen, Tesla, and IDEO. Our investors include Intel, Denso, UPS, Volvo, and Lockheed Martin. Our board members include Ralph Eschenbach, "father of commercial GPS," and Rodney Slater, Former US Secretary of Transportation.
        """
        })
        self.assertIn('C++', c.terms())
        self.assertNotIn('C', c.terms())

        c = submission.Comment({
        'text' : """
        Peloton Technology | Mountain View, CA. | NO REMOTE | Full-time
        """
        })
        self.assertIn('Onsite', c.terms())


if __name__ == '__main__':
    unittest.main()
