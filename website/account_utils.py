import psycopg2

survey_options=[
	"alcohol_cocktail",
	"alcohol_free",
	"celery_free",
	"crustacean_free",
	"dairy_free",
	"DASH",
	"egg_free",
	"fish_free",
	"fodmap_free",
	"gluten_free",
	"immuno_supportive",
	"keto_friendly",
	"kidney_friendly",
	"kosher",
	"low_potassium",
	"low_sugar",
	"lupine_free",
	"Mediterranean",
	"mollusk_free",
	"mustard_free",
	"No_oil_added",
	"paleo",
	"peanut_free",
	"pecatarian",
	"pork_free",
	"red_meat_free",
	"sesame_free",
	"shellfish_free",
	"soy_free",
	"sugar_conscious",
	"sulfite_free",
	"tree_nut_free",
	"vegan",
	"vegetarian",
	"wheat_free",
]
def allfalsemap():
	falsemap={}
	for i in survey_options:
		falsemap[i]=False;
	return falsemap;
def register(first_name,last_name,email,password):
	conn = psycopg2.connect(
	    host="ec2-54-211-177-159.compute-1.amazonaws.com",
	    port="5432",
	    database="d37cnqb90qqaeb",
	    user="bqucvxsqkrxwzh",
	    password="ee7fcdf7a6f6878a2a0c0873a84ac34f9816c92b5d036a1d570e5ee4bdd3ba98"
	)

	cursor=conn.cursor()
	# cursor.execute("select count (*) from Users where email like '{}'".format(email))
	
	# if(cursor.fetchone()[0] !=0):
	# 	cursor.close()
	# 	return {"result":"failed","errormsg":"user email already exists"}
	
	cursor.execute("INSERT INTO Users (firstName, lastName, email, password) values ('{}','{}','{}','{}');".format(first_name,last_name,email,password))

	#print(cursor.fetchall())
	conn.commit()
	cursor.close()
	assert update_settings(email,allfalsemap())["result"]!="failed"
	return {"result":"succeed"}

def update_settings(
	email,
	option_params
	):
	conn = psycopg2.connect(
	    host="ec2-54-211-177-159.compute-1.amazonaws.com",
	    port="5432",
	    database="d37cnqb90qqaeb",
	    user="bqucvxsqkrxwzh",
	    password="ee7fcdf7a6f6878a2a0c0873a84ac34f9816c92b5d036a1d570e5ee4bdd3ba98"
	)

	cursor=conn.cursor()
	cursor.execute("select count (*) from Users where email like '{}'".format(email))
	
	if(cursor.fetchone()[0] ==0):
		cursor.close()
		return {"result":"failed","errormsg":"user does not exist"}

	update_sql="update Users set ";
	for i in survey_options:
		update_sql+=("{}={}".format(i,option_params[i]));
		if(i!=survey_options[-1]):
			update_sql+=(",");
	update_sql+=(" where email like '{}';".format(email))
	#print(update_sql)
	cursor.execute(update_sql);

	conn.commit()
	cursor.close()
	return {"result":"succeed"}

def get_settings(email):
	conn = psycopg2.connect(
	    host="ec2-54-211-177-159.compute-1.amazonaws.com",
	    port="5432",
	    database="d37cnqb90qqaeb",
	    user="bqucvxsqkrxwzh",
	    password="ee7fcdf7a6f6878a2a0c0873a84ac34f9816c92b5d036a1d570e5ee4bdd3ba98"
	)
	cursor=conn.cursor()
	cursor.execute("select count (*) from Users where email like '{}'".format(email))
	if(cursor.fetchone()[0] ==0):
		cursor.close()
		return {"result":"failed","errormsg":"user does not exist"}

	
	cursor.execute("select * from Users where email like '{}'".format(email));
	res=cursor.fetchone();
	#print(res)

	result={}
	for i in range(len(survey_options)):
		result[survey_options[i]]=res[4+i]
	conn.commit()
	cursor.close()
	return {"result":"succeed","data":result};

#print(register("first","last","testuser3@tamu.edu","mypassword"))
#print(update_settings("testuser3@tamu.edu",allfalsemap()))
#print(get_settings("testuser3@tamu.edu"))