import entity1

allowed = {
	'Account' : {
		'create' : {
			'admin' : 'all',
			'eve'	: 'all',
			'john'	: 'owner',
			'mike'  : 'owner'
		},
		'update' : {
			'admin' : 'all',
			'eve'	: 'all',
			'john'	: 'owner',
			'mike'  : 'owner'
		},
		'delete' : {
			'admin' : 'all',
			'eve'	: 'all',
		}
	}
}

def isallowed(action,entity,user,owner):
	if len(owner) < 1 : return True
	try:
		privileges = allowed[entity.__class__.__name__][action]
		if not user in privileges :
			return False
		elif privileges[user] == 'all': 
			return True
		elif privileges[user] == 'owner' and user == owner[0].name:
			return True
		else:
			return False
	except KeyError:
		return True