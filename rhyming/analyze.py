from rhymetagger import RhymeTagger

poem = [
	"Tell me not, in mournful numbers,",
	"Life is but an empty dream!",
	"For the soul is dead that slumbers,",
	"And things are not what they seem.",
	"Life is real! Life is earnest!",
	"And the grave is not its goal;",
	"Dust thou art, to dust returnest,",
	"Was not spoken of the soul.",
	"Not enjoyment, and not sorrow,",
	"Is our destined end or way;",
	"But to act, that each tomorrow",
	"Find us farther than today.",
]

rt = RhymeTagger()
rt.load_model(model='en')

rhymes = rt.tag(poem, output_format=3) 
print(rhymes)

