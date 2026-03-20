import os
import yaml

BASE_DIR = "content"

def make_fm(data):
    return "---\n" + yaml.dump(data, sort_keys=False) + "---\n\n"

def write_file(path, data, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(make_fm(data) + content)

USER_DATA = {
    "alice": {
        "tags": ["distributed-systems", "programming", "go", "linux", "photography"],
        "about": """{{< profile-intro image="/images/alice/headshot.jpg" name="Alice" title="Principal Software Engineer" >}}

Welcome to my slice of the web. I have spent the last decade working on highly available systems, wrangling consensus protocols, and complaining about YAML. In my theoretical free time, I shoot medium-format landscape photography.

## Career History

{{< resume-org name="Global CDN Corp" start="2018" end="Present" >}}
{{< resume-role title="Principal Engineer, Control Plane" period="Jan 2021 - Present" >}}
- Architected the next-generation configuration distribution system using Raft and gRPC.
- Decreased p99 propagation latency from 45s to 2.1s globally.
- Mentored five senior engineers through staff promotion.
{{< /resume-role >}}
{{< resume-role title="Senior Staff Engineer" period="Mar 2018 - Jan 2021" >}}
- Led the migration of legacy C++ load balancers to Go.
{{< /resume-role >}}
{{< /resume-org >}}

{{< resume-org name="StartupHub" start="2014" end="2018" >}}
{{< resume-role title="Backend Developer" period="2014 - 2018" >}}
Built the foundational microservices architecture that scaled the company through Series C.
{{< /resume-role >}}
{{< /resume-org >}}

{{< note title="Need to get in touch?" >}}
I rarely check LinkedIn. Please find my email in the footer.
{{< /note >}}
""",
        "posts": [
            {
                "slug": "understanding-raft", "year": "2024",
                "title": "Understanding the Raft Consensus Algorithm",
                "date": "2024-09-12", "tags": ["distributed-systems", "consensus", "programming"],
                "summary": "A practical walkthrough of leader election and log replication in Raft, with annotated Go examples.",
                "content": """Raft was designed to be understandable. Unlike Paxos, which often feels like reading ancient Greek while standing on your head, Raft splits the consensus problem into three distinct, manageable pieces: leader election, log replication, and safety.

## Leader Election

The core of Raft is the heartbeat mechanism. A leader sends periodic heartbeats to all followers. If a follower doesn't receive a heartbeat within the election timeout, it assumes the leader is dead and starts an election.

{{< tip title="Timer Jitter" >}}
To prevent split votes where every node times out simultaneously, Raft requires randomized election timeouts (e.g., between 150ms and 300ms).
{{< /tip >}}

## The Go Implementation

Here is a simplified look at how a heartbeat loop might be structured in Go using channels and tickers:

{{< highlight-file name="raft_leader.go" lang="go" >}}
func (rf *Raft) heartbeatLoop() {
    ticker := time.NewTicker(75 * time.Millisecond)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            if rf.role == Leader {
                rf.broadcastAppendEntries()
            }
        case <-rf.shutdownCh:
            return
        }
    }
}
{{< /highlight-file >}}

When things go wrong, the logs are your best friend. But nothing replaces a solid understanding of the State Machine Replication fundamentals."""
            },
            {
                "slug": "linux-networking-namespaces", "year": "2024",
                "title": "Demystifying Linux Network Namespaces",
                "date": "2024-03-22", "tags": ["linux", "networking", "containers"],
                "summary": "How Docker actually isolates your networks under the hood.",
                "content": """Containers aren't real. They are just processes with a very specific set of lies told to them by the Linux kernel. The most interesting of these lies is the Network Namespace.

When you create a docker container, you aren't booting a VM. You are just creating an isolated `netns`.

{{< warning title="Kernel Panics" >}}
Do not carelessly delete namespaces if you have active packet captures running on `veth` pairs inside them. Older kernels handle this poorly.
{{< /warning >}}

If you want to create a namespace manually, it's trivial:

{{< highlight-file name="terminal" lang="bash" >}}
ip netns add my_ns
ip netns exec my_ns ip link set lo up
{{< /highlight-file >}}

And just like that, you have an isolated network environment. We build entirely complex orchestrators around this fundamental primitive."""
            },
            {
                "slug": "camera-gear-2023", "year": "2023",
                "title": "My Landscape Photography Kit for 2023",
                "date": "2023-11-05", "tags": ["photography", "gear"],
                "summary": "What's in my bag for remote hiking and landscape shoots.",
                "content": """For the last three years, I've been optimizing my kit for weight without sacrificing dynamic range. When you're hiking 15 miles into the back country, every ounce matters.

## The Core Kit

{{< list-columns cols="2" >}}
- Fujifilm GFX 50S II
- GF 32-64mm f/4 R LM WR
- GF 100-200mm f/5.6 R LM OIS WR
- Gitzo Traveler Tripod
- Nisi V7 Filter Holder
- 10-stop ND Filter
- Garmin inReach Mini 2
- Lots of extra batteries
{{< /list-columns >}}

{{< caution title="Weather Sealing" >}}
"Weather-resistant" does not mean waterproof. Always carry a dry bag for unexpected downpours.
{{< /caution >}}"""
            },
            {
                "slug": "why-go", "year": "2023",
                "title": "Why We Migrated to Go",
                "date": "2023-06-12", "tags": ["programming", "go"],
                "summary": "Reflections on our transition from C++ to Go for the control plane.",
                "content": """Two years ago, we made the controversial decision to halt all new feature development in our C++ codebase and rewrite the entire control plane load balancer in Go. 

It was painful. It was expensive. It was absolutely the right choice.

The biggest win wasn't execution speed—it was deployment velocity. Our compile times dropped from 45 minutes to 30 seconds. Onboarding a new engineer dropped from two months to two weeks. 

We sacrificed a marginal amount of CPU efficiency for a massive gain in developer throughput."""
            },
            {
                "slug": "the-myth-of-rest", "year": "2025",
                "title": "The Myth of REST",
                "date": "2025-01-14", "tags": ["programming", "distributed-systems"],
                "summary": "Why your JSON API is just RPC over HTTP.",
                "content": """Nobody uses REST. Not really. 

Roy Fielding's dissertation described a highly decoupled, hypermedia-driven architecture where clients navigate state transitions via HATEOAS. What you built is RPC with HTTP verbs. And that is fine.

We need to stop pretending that using `POST /api/users/123/activate` is RESTful. It isn't. It's an RPC call telling the server to execute an action. 

Embrace RPC paradigms where they make sense. Use gRPC for internal service-to-service communication, and provide a GraphQL or JSON-RPC layer to the frontend. Stop twisting HTTP protocols into weird shapes."""
            }
        ],
        "galleries": [
            {
                "slug": "yosemite-winter", "date": "2024-02-15",
                "title": "Yosemite in Winter", "summary": "A collection of stark, snowy landscapes from the valley floor.",
                "image": "/images/alice/gallery/yosemite-1.jpg", "thumbnail": "/images/alice/gallery/yosemite-thumb.jpg",
                "metadata": {"camera": "GFX 50S II", "lens": "32-64mm", "location": "Yosemite National Park", "season": "Winter"},
                "content": "These photos were taken over a three-day snowstorm in February. The contrast between the dark granite and the fresh powder was incredible.\n\n{{< showcase image=\"/images/alice/gallery/yosemite-2.jpg\" >}}\nHalf Dome clearing from the storm clouds at sunset. The light only lasted for about three minutes before fading entirely.{{< /showcase >}}"
            },
            {
                "slug": "death-valley", "date": "2023-11-10",
                "title": "Death Valley Dunes", "summary": "Abstract geometries formed by wind and sand.",
                "image": "/images/alice/gallery/dunes-1.jpg", "thumbnail": "/images/alice/gallery/dunes-thumb.jpg",
                "metadata": {"camera": "GFX 50S II", "lens": "100-200mm", "location": "Mesquite Flat Sand Dunes", "time": "Sunrise"},
                "content": "The key to dune photography is focal length compression. I used a telephoto to flatten the ripples against each other."
            },
            {
                "slug": "iceland-highlands", "date": "2023-08-20",
                "title": "Icelandic Highlands", "summary": "Braided rivers and volcanic ash.",
                "image": "/images/alice/gallery/iceland-1.jpg", "thumbnail": "/images/alice/gallery/iceland-thumb.jpg",
                "metadata": {"camera": "GFX 50S II", "location": "Landmannalaugar", "format": "Medium Format"},
                "content": "Shot from a Cessna over the highlands. The braided rivers look like veins carrying glacial melt to the sea."
            },
            {
                "slug": "pnw-coast", "date": "2024-06-05",
                "title": "Pacific Northwest Coast", "summary": "Sea stacks and fog.",
                "image": "/images/alice/gallery/pnw-1.jpg", "thumbnail": "/images/alice/gallery/pnw-thumb.jpg",
                "metadata": {"camera": "X-T5", "location": "Rialto Beach"},
                "content": "Heavy fog rolling in over the sea stacks at low tide."
            },
            {
                "slug": "redwoods", "date": "2024-05-12",
                "title": "Redwood Canopies", "summary": "Looking up into ancient giants.",
                "image": "/images/alice/gallery/redwoods.jpg", "thumbnail": "/images/alice/gallery/redwoods-thumb.jpg",
                "metadata": {"camera": "GFX 50S II", "location": "Jedediah Smith State Park"},
                "content": "The scale is impossible to convey, but I tried."
            },
            {
                "slug": "sierra-granite", "date": "2025-01-02",
                "title": "High Sierra Granite", "summary": "Sharp peaks at 12,000 feet.",
                "image": "/images/alice/gallery/sierra.jpg", "thumbnail": "/images/alice/gallery/sierra-thumb.jpg",
                "metadata": {"camera": "X-T5", "location": "Kings Canyon"},
                "content": "The high country in late summer."
            }
        ]
    },
    "bob": {
         "about": """{{< profile-intro image="/images/bob/headshot.jpg" name="Bob" title="Baker & Woodworker" >}}
I make bread, and when I'm waiting for the dough to rise, I build furniture.

I believe in learning in public. When I mess up a dovetail joint or over-proof a loaf, I put it here so others can learn from my mistakes.

## My Workshop

{{< list-columns cols="2" >}}
- DeWalt Table Saw
- Veritas Low Angle Jack Plane
- Lie-Nielsen router plane
- 6-quart cast iron Dutch oven
- Lodge combo cooker
- Very sharp chisels
{{< /list-columns >}}

{{< important title="Safety First" >}}
Woodworking tools are inherently dangerous. Never bypass safety guards, and always use push sticks. 
{{< /important >}}
""",
        "posts": [
            {
                "slug": "first-dovetails", "year": "2024",
                "title": "My First Attempt at Hand-Cut Dovetails",
                "date": "2024-02-14", "tags": ["learning", "woodworking", "tools"],
                "summary": "They are ugly, gappy, and I am incredibly proud of them.",
                "content": """Dovetails are the hallmark of fine woodworking, or so everyone says. I finally bought a decent backsaw and gave it a try.

The result was a rather loose, structurally questionable joint. But it held!

{{< tip title="Marking Out" >}}
Use a marking knife, not a pencil. A pencil line has thickness. A knife wall gives your chisel a physical reference to index against.
{{< /tip >}}

I realized that my sawing technique was the main issue. I wasn't dropping my elbow, so the saw was drifting off plum. Practice makes slightly better."""
            },
            {
                "slug": "sourdough-hydration", "year": "2023",
                "title": "Understanding Sourdough Hydration",
                "date": "2023-08-10", "tags": ["baking", "learning", "sourdough"],
                "summary": "Why 80% hydration isn't always better than 70%.",
                "content": """When you start baking sourdough, there is a macho culture around pushing hydration as high as possible. Everyone wants that wide-open, lacy crumb.

I spent six months frustrating myself with soupy doughs that I couldn't shape, resulting in flat, dense frisbees.

Then I watched a video by a master baker who said: "A good 70% loaf beats a failed 85% loaf every time."

I dropped my water content down to 72%. Suddenly, I could build tension during shaping. The loaf sprang in the oven. The crumb wasn't glass-like, but it was light, airy, and practical for making sandwiches."""
            },
            {
                "slug": "milling-my-own-flour", "year": "2024",
                "title": "Milling My Own Flour",
                "date": "2024-11-05", "tags": ["baking", "tools", "sourdough"],
                "summary": "The countertop grain mill was a game changer.",
                "content": """Freshly milled flour fundamentally changes the fermentation profile of your starter. 

{{< note title="The Equipment" >}}
I picked up a Mockmill 100 stone mill. It produces incredibly fine whole grain flour without heating the grain too much.
{{< /note >}}

The aroma of freshly milled Yecora Rojo wheat is sweet and cinnamon-like. The loaves I'm getting now have a much more complex crust flavor."""
            },
            {
                "slug": "building-a-workbench", "year": "2023",
                "title": "Building the Roubo Workbench",
                "date": "2023-01-20", "tags": ["woodworking", "projects", "tools"],
                "summary": "A heavy bench makes everything else easier.",
                "content": """You can't do good hand tool work on a wobbly table. 

I spent a month laminating 2x4s into a massive 4-inch thick slab for a traditional French Roubo workbench. It weighs roughly 350 pounds. 

When you plane a board on this bench, the bench doesn't move. At all. It has transformed my woodworking."""
            },
            {
                "slug": "sharpening-chisels", "year": "2025",
                "title": "The Zen of Sharpening",
                "date": "2025-01-05", "tags": ["woodworking", "tools", "learning"],
                "summary": "Why I abandoned sharpening jigs and learned to freehand.",
                "content": """Sharpening jigs guarantee a perfect secondary bevel. They also take 5 minutes to set up.

If it takes 5 minutes to set up the jig, you will keep using a dull chisel for another 10 minutes rather than stop to sharpen. This is a false economy.

I forced myself to learn freehand sharpening on diamond stones. It takes 30 seconds. I touch up my blades constantly now, meaning they are always razor sharp."""
            }
        ]
    },
    "carol": {
        "about": """{{< profile-intro image="/images/carol/headshot.jpg" name="Carol" title="Textile Artist & Quilter" >}}
I have been sewing since I was nine years old. After thirty years teaching secondary mathematics, I retired and turned my focus entirely to textile geometry.

My work explores traditional block structures reimagined with modern, high-contrast color palettes.

## Exhibitions & Guilds

{{< resume-org name="Modern Quilt Guild" start="2012" end="Present" >}}
{{< resume-role title="Board Member, Regional Chapter" period="2018 - 2022" >}}
Organized three regional symposiums on color theory and precision piecing.
{{< /resume-role >}}
{{< /resume-org >}}

{{< resume-org name="National Quilt Symposium" start="2015" end="2015" >}}
{{< resume-role title="Juried Exhibitor" period="July 2015" >}}
Exhibited 'Fractured Light', a 72x90 medallion quilt.
{{< /resume-role >}}
{{< /resume-org >}}

{{< note title="Commissions" >}}
I am not accepting commission work at this time. I am focusing entirely on exhibition pieces.
{{< /note >}}
""",
        "tags": ["quilting", "color", "design", "learning"],
        "posts": [
            {
                "slug": "color-value", "year": "2023",
                "title": "Value Does All the Work",
                "date": "2023-04-10", "tags": ["color", "design", "quilting"],
                "summary": "Color gets the credit, but value does the work.",
                "content": """When a quilt looks flat or muddy, the piecer usually blames their color choices. Ninety percent of the time, the colors are fine. The problem is a lack of value contrast.

If you take a photo of your fabrics and put a black-and-white filter on it, do they all merge into a medium gray? If so, your pattern will disappear.

{{< tip title="The Value Finder Tool" >}}
Keep a piece of red transparent acrylic in your sewing room. By looking through it, you eliminate hue and can see the true value of your fabrics.
{{< /tip >}}

Always include a strong dark and a clear light."""
            },
            {
                "slug": "precision-piecing", "year": "2024",
                "title": "In Defense of Pinning",
                "date": "2024-05-18", "tags": ["quilting", "technique", "tools"],
                "summary": "Why the modern 'no-pin' trend sacrifices accuracy.",
                "content": """There is a current trend on Instagram of sewing long seams without pins, relying entirely on tension and hand position. 

This works for garments or large bags. It is disastrous for a complicated block with nested seams.

When you have six points converging in the center of a Lone Star block, an eighth of an inch of drift will ruin the entire star. Pin your seams. Press open when there's bulk. Accuracy is respect for your own time."""
            },
            {
                "slug": "drafting-patterns", "year": "2023",
                "title": "Mathematics in Quilt Drafting",
                "date": "2023-10-02", "tags": ["design", "learning", "quilting"],
                "summary": "Using simple geometry to scale blocks.",
                "content": """My background is in mathematics, which is perhaps why drafting block scale is my favorite part of the process.

If you have a block that finishes at 9 inches, the diagonal is 12.72 inches (using the Pythagorean theorem). If you want to set those blocks on point, your setting triangles must account for that diagonal, plus seam allowances.

Don't be afraid of the math. It prevents wasted fabric."""
            },
            {
                "slug": "thread-weight", "year": "2024",
                "title": "Choosing Quilt Thread Weight",
                "date": "2024-01-15", "tags": ["quilting", "tools", "materials"],
                "summary": "When to use 50wt versus 40wt thread.",
                "content": """For piecing, I exclusively use 50-weight cotton thread (specifically Aurifil). It's incredibly strong but thin enough that it doesn't add bulk to your seams.

For the actual quilting (stitching the layers together), thread weight is a design choice.

{{< list-columns cols="2" >}}
- 50wt: Blends in beautifully, lets the piecing shine.
- 40wt: Noticeable, gives great texture.
- 28wt or 12wt: Bold. Used for hand-quilting and heavy topstitching. Looks like embroidery.
{{< /list-columns >}}
"""
            },
            {
                "slug": "quiltcon-2025", "year": "2025",
                "title": "Thoughts on QuiltCon 2025",
                "date": "2025-02-28", "tags": ["quilting", "events", "design"],
                "summary": "A recap of the trends and standout pieces from the show.",
                "content": """The most striking trend at this year's convention was the overwhelming use of negative space explicitly integrated into the block structures, rather than just as a border.

It requires tremendous discipline to leave three square feet of a quilt top entirely blank.

I left the show incredibly uninspired by the commercial vendor hall, but deeply moved by the artistry in the exhibition wings."""
            }
        ],
        "galleries": [
            {
                "slug": "midnight-star", "date": "2022-11-20",
                "title": "Midnight Star", "summary": "A 72-inch Lone Star quilt in navy and gold.",
                "image": "/images/carol/gallery/midnight-star.jpg", "thumbnail": "/images/carol/gallery/midnight-star-thumb.jpg",
                "metadata": {"dimensions": "72 x 72 inches", "technique": "Foundation paper pieced", "materials": "Kona Cotton"},
                "content": "A central lone star heavily relying on value-gradation to simulate a glowing effect."
            },
            {
                "slug": "city-grid", "date": "2023-01-15",
                "title": "City Grid", "summary": "Abstract improvisational piecing reflecting urban density.",
                "image": "/images/carol/gallery/city-grid.jpg", "thumbnail": "/images/carol/gallery/city-grid-thumb.jpg",
                "metadata": {"dimensions": "60 x 80 inches", "technique": "Improv piecing", "quilted_by": "Carol User"},
                "content": "No rulers were used in the making of this top."
            },
            {
                 "slug": "fractured-light", "date": "2015-07-01",
                 "title": "Fractured Light", "summary": "A complex medallion quilt.",
                 "image": "/images/carol/gallery/fractured.jpg", "thumbnail": "/images/carol/gallery/fractured-thumb.jpg",
                 "metadata": {"dimensions": "72 x 90 inches", "exhibited": "National Quilt Symposium 2015"},
                 "content": "My first major exhibition piece."
             },
             {
                 "slug": "autumn-path", "date": "2023-10-15",
                 "title": "Autumn Path", "summary": "Flying geese in earth tones.",
                 "image": "/images/carol/gallery/autumn.jpg", "thumbnail": "/images/carol/gallery/autumn-thumb.jpg",
                 "metadata": {"dimensions": "50 x 60 inches", "technique": "Traditional piecing"},
                 "content": "A study in rust, ochre, and deep brown."
             },
             {
                 "slug": "blue-glass", "date": "2024-03-10",
                 "title": "Blue Glass", "summary": "Half-square triangles forming a shattered glass motif.",
                 "image": "/images/carol/gallery/blue-glass.jpg", "thumbnail": "/images/carol/gallery/blue-glass-thumb.jpg",
                 "metadata": {"dimensions": "80 x 80 inches", "materials": "Oakshott shot cottons"},
                 "content": "The warp and weft of the shot cottons give this quilt a luminous quality depending on viewing angle."
             },
             {
                 "slug": "winter-solstice", "date": "2024-12-21",
                 "title": "Winter Solstice", "summary": "Minimalist curves in black, white, and silver.",
                 "image": "/images/carol/gallery/solstice.jpg", "thumbnail": "/images/carol/gallery/solstice-thumb.jpg",
                 "metadata": {"dimensions": "40 x 40 inches", "technique": "Curved piecing"},
                 "content": "An exercise in extreme restraint."
             }
        ]
    },
    "dave": {
        "about": """{{< profile-intro image="/images/dave/headshot.jpg" name="Dave" title="Travel Photographer" >}}
I've lived out of a unified carry-on bag since 2017. Previously a commercial photographer in London, I traded the studio for the road.

I document emerging urban hubs and fading analog traditions.

## Background

{{< resume-org name="Freelance Editorial" start="2017" end="Present" >}}
{{< resume-role title="Contributing Photographer" period="2017 - Present" >}}
Assignments and licensing for travel and documentary publications.
{{< /resume-role >}}
{{< /resume-org >}}

{{< resume-org name="London Creative Studio" start="2010" end="2017" >}}
{{< resume-role title="Studio Manager & Lead Photographer" period="2013 - 2017" >}}
Managed a team of four lighting assistants and handled key commercial accounts.
{{< /resume-role >}}
{{< /resume-org >}}
""",
        "tags": ["photography", "travel", "gear", "writing"],
        "posts": [
            {
                "slug": "one-bag-travel", "year": "2023",
                "title": "One Bag Travel for Photographers",
                "date": "2023-02-15", "tags": ["travel", "photography", "gear"],
                "summary": "How to pack camera gear for indefinite travel without checking a bag.",
                "content": """Airlines lose bags. That is an immutable law of physics. If your livelihood depends on your gear arriving when you do, you cannot check it.

This means fitting your clothes, laptop, and camera kit into a 40L bag that fits in the overhead bin.

{{< important title="Weight Limits" >}}
Airlines in Asia frequently weigh carry-on bags. The limit is often 7kg. My camera and laptop alone weigh 3.5kg. Choose your lenses carefully.
{{< /important >}}

I carry one body (Sony A7C) and two prime lenses (35mm and 85mm). No zooms. The limitation breeds creativity."""
            },
            {
                "slug": "street-photography-ethics", "year": "2024",
                "title": "The Ethics of Street Photography",
                "date": "2024-05-19", "tags": ["photography", "writing", "travel"],
                "summary": "Taking photos of strangers abroad.",
                "content": """There is a fine line between documenting a culture and exploiting it.

When you walk through a market with a massive 70-200mm lens mounted to your eye like a sniper rifle, you fundamentally alter the atmosphere around you. You aren't observing the market; the market is observing you.

I use a 35mm lens. It forces me to get close. I smile, I make eye contact, and if someone shakes their head, I put the camera down."""
            },
            {
                "slug": "editing-philosophy", "year": "2023",
                "title": "My Post-Processing Philosophy",
                "date": "2023-09-08", "tags": ["photography", "learning", "tools"],
                "summary": "Why less is usually more in Lightroom.",
                "content": """The sliders in Lightroom are dangerously powerful. It's incredibly easy to push the clarity, crush the blacks, and bump the vibrance until the image looks like a plastic rendering.

My rule is to edit until the image matches what my eye saw on location.

{{< note title="The Final Pass" >}}
Once I finish an edit, I walk away for 24 hours. When I come back, I usually dial everything back by 15%.
{{< /note >}}"""
            },
            {
                "slug": "hanoi-traffic", "year": "2024",
                "title": "The Choreography of Hanoi Traffic",
                "date": "2024-11-20", "tags": ["travel", "writing"],
                "summary": "Finding the rhythm in chaos.",
                "content": """To cross a street in Hanoi is an act of faith. You do not wait for a gap, because there are no gaps. There is only a continuous, flowing river of mopeds.

You step off the curb. You walk at a steady, predictable pace. You do not stop, and you absolutely never step backward. The mopeds will flow around you like water around a stone. It is terrifying the first time, and exhilarating the fiftieth."""
            },
            {
                "slug": "why-shoot-film", "year": "2025",
                "title": "Why I Still Carry a Leica M6",
                "date": "2025-01-10", "tags": ["photography", "gear", "film"],
                "summary": "Analog photography in a digital nomad's bag.",
                "content": """Film is expensive, heavy, x-ray sensitive, and slow. Why do I carry a brick of Ilford HP5+ in my limited bag space?

Because film forces intention. 

When every shutter click costs a dollar, you stop spraying and praying. You meter the light. You wait for the subject to step precisely into the frame. You actually *look* at the scene instead of chimping the LCD screen."""
            }
        ],
         "galleries": [
            {
                "slug": "kyoto-rain", "date": "2023-04-12",
                "title": "Kyoto in the Rain", "summary": "Neon reflections and umbrellas in Pontocho Alley.",
                "image": "/images/dave/gallery/kyoto-1.jpg", "thumbnail": "/images/dave/gallery/kyoto-thumb.jpg",
                "metadata": {"location": "Kyoto, Japan", "film": "Cinestill 800T", "camera": "Leica M6"},
                "content": "Rain entirely shifts the color palette of neon cities from harsh white to diffused cyan and magenta."
            },
            {
                "slug": "hanoi-markets", "date": "2024-11-25",
                "title": "Morning Market, Hanoi", "summary": "Vendors at 5:00 AM.",
                "image": "/images/dave/gallery/hanoi-1.jpg", "thumbnail": "/images/dave/gallery/hanoi-thumb.jpg",
                "metadata": {"location": "Hanoi, Vietnam", "camera": "Sony A7C", "lens": "35mm f/1.4"},
                "content": "The best pictures in Southeast Asia happen before the sun is fully up."
            },
            {
                 "slug": "mongolian-steppe", "date": "2023-08-05",
                 "title": "Nomadic Herders", "summary": "Portraits from the Mongolian steppe.",
                 "image": "/images/dave/gallery/mongolia.jpg", "thumbnail": "/images/dave/gallery/mongolia-thumb.jpg",
                 "metadata": {"location": "Mongolia", "camera": "Sony A7C"},
                 "content": "A family that hosted us during a severe storm."
            },
            {
                 "slug": "cairo-dust", "date": "2024-02-18",
                 "title": "Cairo Dust", "summary": "Silhouettes in the Islamic Quarter.",
                 "image": "/images/dave/gallery/cairo.jpg", "thumbnail": "/images/dave/gallery/cairo-thumb.jpg",
                 "metadata": {"location": "Cairo, Egypt", "camera": "Leica M6", "film": "Tri-X 400"},
                 "content": "The particulate dust scatters the late afternoon light beautifully."
            },
            {
                 "slug": "lisbon-trams", "date": "2024-09-10",
                 "title": "Alfama Lines", "summary": "Tram 28 navigating impossible hills.",
                 "image": "/images/dave/gallery/lisbon.jpg", "thumbnail": "/images/dave/gallery/lisbon-thumb.jpg",
                 "metadata": {"location": "Lisbon, Portugal", "camera": "Sony A7C"},
                 "content": "{{< showcase image=\"/images/dave/gallery/lisbon-2.jpg\" >}}\nTiming the tram perfectly between two parked cars on a 20-degree incline.{{< /showcase >}}"
            },
            {
                 "slug": "patagonia", "date": "2025-02-01",
                 "title": "Fitz Roy", "summary": "Alpenglow over the dominant peak.",
                 "image": "/images/dave/gallery/fitz.jpg", "thumbnail": "/images/dave/gallery/fitz-thumb.jpg",
                 "metadata": {"location": "El Chalten, Argentina", "lens": "85mm f/1.8"},
                 "content": "We waited three days for the legendary cloud cover to break. It broke for exactly twenty minutes."
            }
        ]
    },
    "eve": {
        "about": """{{< profile-intro image="/images/eve/headshot.jpg" name="Eve" title="Security Researcher" >}}
I break things. Usually cryptography, sometimes hypervisors. 

I speak at conferences about vulnerability research and the sheer terrifying fragility of the modern web.

## Security Roles

{{< resume-org name="Cipher Labs" start="2021" end="Present" >}}
{{< resume-role title="Lead Vulnerability Researcher" period="Mar 2021 - Present" >}}
- Discovered and responsibly disclosed CVE-2022-XXXX, CVE-2023-YYYY.
- Lead the zero-day impact analysis team.
{{< /resume-role >}}
{{< /resume-org >}}

{{< resume-org name="Tech Megacorp" start="2016" end="2021" >}}
{{< resume-role title="Product Security Engineer" period="2016 - 2021" >}}
Built internal fuzzing infrastructure that scaled across 10,000 repositories.
{{< /resume-role >}}
{{< /resume-org >}}

{{< caution title="Bounty Policy" >}}
I do not provide free consulting or participate in low-payout bug bounties.
{{< /caution >}}
""",
        "tags": ["linux", "programming", "hardware", "security", "writing"],
        "posts": [
            {
                "slug": "state-of-fuzzing", "year": "2023",
                "title": "The State of Fuzzing in 2023",
                "date": "2023-06-11", "tags": ["security", "programming", "linux"],
                "summary": "Why AFL++ is still the king, and where symbolic execution falls short.",
                "content": """Fuzzing is the most brutally effective way to find memory corruption bugs in large C/C++ codebases. Period.

While academic papers love symbolic execution, nothing beats the throughput of a well-instrumented generational fuzzer like AFL++. You just throw CPU cycles at the problem until a segfault shakes out.

{{< highlight-file name="harness.c" lang="c" >}}
#include <stdint.h>
#include <stddef.h>

int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  // Your target API here
  ParseImage(Data, Size);
  return 0;
}
{{< /highlight-file >}}

If you haven't fuzzed your parser, it is vulnerable."""
            },
            {
                "slug": "hardware-attacks", "year": "2024",
                "title": "Introduction to Hardware Fault Injection",
                "date": "2024-03-05", "tags": ["security", "hardware"],
                "summary": "Bypassing secure boot with precisely timed voltage glitches.",
                "content": """Software security assumes the hardware reliably executes the instructions it is given. Fault injection attacks (glitching) prove that this assumption is a lie.

If you drop the CPU core voltage for exactly 50 nanoseconds precisely when it's reading the 'SecureBoot=True' register, the CPU will read a 0 instead of a 1. 

{{< warning title="Bricked Devices" >}}
You will destroy hardware doing this. Buy spares. Don't glitch the only prototype.
{{< /warning >}}

It requires an oscilloscope, an FPGA, and a lot of patience. But seeing a root shell pop over UART on a locked device is pure magic."""
            },
            {
                "slug": "defcon-32", "year": "2024",
                "title": "DEF CON 32 Recap",
                "date": "2024-08-15", "tags": ["security", "events", "writing"],
                "summary": "Line-con, broken elevators, and some genuinely brilliant talks.",
                "content": """Every year I say I'm not going back to DEF CON, and every year I end up in Las Vegas in August suffering through 110-degree heat and hotel Wi-Fi.

The standout talk this year wasn't on the main stage; it was a deeply technical breakdown of baseband exploitation in the hardware village.

The culture feels slightly more corporate every year, but the raw talent of the community remains undeniable."""
            },
            {
                "slug": "c-memory-safety", "year": "2023",
                "title": "C memory safety will never happen",
                "date": "2023-11-20", "tags": ["programming", "security"],
                "summary": "Temporal safety cannot be bolted onto C retroactively.",
                "content": """Spatial memory safety in C (bounds checking) is extremely difficult but theoretically possible with hardware assistance like ARM MTE.

Temporal memory safety (use-after-free) in C is fundamentally impossible without massive performance overhead or a different language paradigm altogether.

Stop writing new network-facing parsers in C. It is professional negligence in the modern era."""
            },
            {
                "slug": "threat-modeling", "year": "2025",
                "title": "Functional Threat Modeling",
                "date": "2025-02-12", "tags": ["security", "writing", "learning"],
                "summary": "How to pragmatically evaluate risk in architecture designs.",
                "content": """Threat modeling usually devolves into a miserable three-hour meeting where engineers argue about nation-state actors rappelling through server room skylights.

Pragmatic threat modeling requires identifying the actual assets, the likely adversaries (usually opportunistic ransomware gangs or insiders), and applying standard mitigations. 

{{< tip title="STRIDE" >}}
Use the STRIDE model (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) simply as a checklist, not a religion.
{{< /tip >}}"""
            }
        ]
    },
    "frank": {
        "about": """{{< profile-intro image="/images/frank/headshot.jpg" name="Frank" title="Retro Hardware Restorer" >}}
I buy broken 16-bit consoles from Yahoo Auctions Japan, recap their motherboards, and bring them back to life.

My garage smells permanently of rosin core solder and yellowing ABS plastic.

## Hobby Pedigree

{{< resume-org name="Self-Taught Workbench" start="2010" end="Present" >}}
{{< resume-role title="Hardware Tinkerer" period="2010 - Present" >}}
- Successfully recapped over 200 Sega Game Gears.
- Developed the open-source RGB mod guide for the PC Engine.
{{< /resume-role >}}
{{< /resume-org >}}

{{< list-columns cols="2" >}}
- Hakko FX-951 Solder Station
- JBC Hot-Air Rework Station
- Rigol DS1054Z Oscilloscope
- 99.9% Isopropyl Alcohol
- RetroTINK 5X-Pro
- A CRT television that weighs 180 lbs
{{< /list-columns >}}
""",
        "tags": ["hardware", "tools", "learning", "programming", "retro"],
        "posts": [
            {
                "slug": "capacitor-plague", "year": "2023",
                "title": "Surviving the Capacitor Plague",
                "date": "2023-05-18", "tags": ["hardware", "retro"],
                "summary": "Why every Sega Game Gear from the 90s is dying, and how to fix it.",
                "content": """Sega used notoriously cheap surface-mount electrolytic capacitors in the early 90s. Today, thirty years later, almost every original Game Gear has leaky caps that destroy the audio, dim the screen, and eventually eat through the PCB traces.

If you buy an 'untested' Game Gear on eBay, you are buying a broken Game Gear.

{{< highlight-file name="supplies.txt" lang="text" >}}
Required:
- 10uF 16v SMD Caps
- 47uF 6.3v SMD Caps
- 100uF 6.3v SMD Caps
- Flux (do not skimp on flux)
{{< /highlight-file >}}

Recapping isn't hard, but cleaning the corrosive fish-smelling electrolyte off the board takes patience."""
            },
            {
                "slug": "crt-geometry", "year": "2024",
                "title": "The Dark Art of CRT Geometry Adjustment",
                "date": "2024-02-05", "tags": ["hardware", "retro"],
                "summary": "Navigating the hidden service menus of late-90s Sony Trinitrons.",
                "content": """A flat-panel OLED is objectively superior in every measurable metric. It also looks entirely wrong for 240p sprite graphics. Retro games were designed with scanlines, shadow masks, and phosphor glow in mind.

Getting a perfect picture requires a Consumer CRT. I recently picked up a Sony KV-27FS120.

{{< caution title="High Voltage" >}}
The flyback transformer in a CRT holds thousands of volts long after the TV is unplugged. Never open the shell unless you know how to safely discharge the tube.
{{< /caution >}}

Fixing the horizontal bowing and overscan required diving into the terrifying 11-button-press sequence to access the service menu."""
            },
            {
                "slug": "optical-drive-emulation", "year": "2024",
                "title": "ODEs and the Future of Disc Preservation",
                "date": "2024-09-12", "tags": ["hardware", "tools", "learning"],
                "summary": "When lasers die, ODEs take over.",
                "content": """The lasers in the Sega Saturn and PlayStation 1 are failing. Soon, every original optical drive will die.

Optical Drive Emulators (ODEs) like the TerraOnion MODE and the XStation bypass the physical laser assembly and feed binary disc images straight to the console's memory bus via SD card.

It is the absolute best way to play original hardware without subjecting valuable original media to wear and tear. It also dramatically improves load times."""
            },
            {
                "slug": "fpga-vs-software", "year": "2023",
                "title": "FPGA Emulation: The MiSTer Project",
                "date": "2023-11-30", "tags": ["programming", "hardware", "retro"],
                "summary": "Why cycle-accurate hardware emulation is replacing RetroArch.",
                "content": """Software emulation runs a program on your CPU that pretends to be a Super Nintendo. An FPGA (Field-Programmable Gate Array) is a blank microchip configured to physically wire itself into the exact logic gates of a Super Nintendo.

The MiSTer project uses an Altera Cyclone V FPGA to achieve cycle-accurate recreation of dozens of classic arcade and console cores.

There is zero input lag, because there is no OS scheduling overhead. It is a stunning triumph of reverse-engineering and open-source collaboration."""
            },
            {
                "slug": "soldering-mistakes", "year": "2025",
                "title": "My Biggest Soldering Mistakes",
                "date": "2025-03-01", "tags": ["tools", "learning", "hardware"],
                "summary": "Lifted pads and burned thumbs.",
                "content": """When I started, I used a $15 soldering iron that plugged directly into the wall with no temperature control. I destroyed so many innocent motherboards.

{{< tip title="Use More Flux" >}}
If your solder joint looks dull, spiky, or won't stick, you need more flux. Plumbers flux is not acceptable. Use no-clean rosin flux meant for electronics.
{{< /tip >}}

A good temperature-controlled iron (like the Pinecil or a Hakko) and high-quality 63/37 leaded solder will immediately make you a 50% better technician."""
            }
        ]
    }
}

for u, data in USER_DATA.items():
    # About
    write_file(os.path.join(BASE_DIR, u, "about", "index.md"), {
        "title": f"About {u.title()}",
        "date": "2024-01-01",
        "draft": False,
        "summary": "Learn more about my background and experience."
    }, data["about"])
    
    # Posts
    for p in data["posts"]:
        fm = {
            "title": p["title"],
            "date": p["date"],
            "draft": False,
            "tags": p["tags"],
            "summary": p["summary"]
        }
        write_file(os.path.join(BASE_DIR, u, "blog", p["year"], p["slug"], "index.md"), fm, p["content"])
        
    # Galleries
    galleries = data.get("galleries", [])
    for g in galleries:
        fm = {
            "title": g["title"],
            "date": g["date"],
            "draft": False,
            "image": g["image"],
            "thumbnail": g["thumbnail"],
            "summary": g["summary"],
            "metadata": g["metadata"]
        }
        write_file(os.path.join(BASE_DIR, u, "gallery", g["slug"], "index.md"), fm, g["content"])

# Disclaimer
write_file(os.path.join(BASE_DIR, "disclaimer.md"), {
    "title": "Legal Disclaimer",
    "date": "2024-01-01",
    "draft": False,
    "layout": "single"
}, "This site is for demonstration purposes only. All content is generated dummy text.\n")

print("High quality content generation complete.")
