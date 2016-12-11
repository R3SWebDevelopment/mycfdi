from mycfdi.lib.decorators import render

def cfdi(template = None , content_type = None , **kwargs):
	path = 'cfdi'
	template = "%s/%s" % (path , template)
	return render(path = template , content_type = content_type , **kwargs)

@cfdi(template="home.html", content_type="html")
def home(request):
    return{
		'data':'hola'
	}