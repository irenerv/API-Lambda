import json
from connection import connectDB

def lambda_handler(event, context):
    path = event['rawPath']
    connection = connectDB()
    cursor = connection.cursor()
    
    if path == "/songs":
        #METHOD: GET all

        try:
            cursor.execute('SELECT * FROM Song')
            rows = cursor.fetchall()

            return {'statusCode': 200,'body': json.dumps(rows)}
        except Exception as e:
            return {"Error": "In GET all " + str(e)}

    if path == "/song":
        #METHOD: GET by ID

        try:
            id = event['queryStringParameters']['id']
            cursor.execute(f'SELECT * FROM Song WHERE song_id = {id}')
            rows = cursor.fetchall()

            return {'statusCode': 200,'body': json.dumps(rows)}
        except Exception as e:
            return {"Error": "In GET by id  " + str(e)}
            
    if path == "/postSong":
        #METHOD: POST

        try:
            #Obtaining body values
            body = json.loads(event['body'])
            name = body['song']['name']
            launched_year = body['song']['launched_year']
            album = body['song']['album']
            author = body['song']['author']
            genre = body['song']['genre']

            sql = f'INSERT INTO `Song` (`name`, `launched_year`, `album`, `author`, `genre`) VALUES(%s, %s, %s, %s, %s)'
            cursor.execute(sql, (name, launched_year, album, author, genre))
            
            #Commit to save changes
            connection.commit()
            return {"Message": "Song recorded successfully"}
        except Exception as e:
            return {"Error": "In POST " + str(e)}
            
    if path == "/putSong":
        #METHOD: UPDATE

        try:
            id = event['queryStringParameters']['id']
            cursor.execute(f'SELECT * FROM Song WHERE song_id = {id}')
            rows = cursor.fetchall()
            
            #Obtaining body values
            body = json.loads(event['body'])
            name = body['song']['name'] if body['song']['name'] is not None  else rows[0]["name"]
            launched_year = body['song']['launched_year'] if body['song']['launched_year'] is not None else rows[0]["launched_year"]
            album = body['song']['album'] if body['song']['album'] is not None else rows[0]["album"]
            author = body['song']['author'] if body['song']['author'] is not None else rows[0]["author"]
            genre = body['song']['genre'] if body['song']['genre'] is not None else rows[0]["genre"]
            
            sql = f'UPDATE `Song` SET `name`=%s, `launched_year`=%s, `album`=%s, `author`=%s, `genre`=%s WHERE `song_id`={id}'
            cursor.execute(sql, (name, launched_year, album, author, genre))
            
            #Commit to save changes
            connection.commit()
            
            #Retrieve new record
            cursor.execute(f'SELECT * FROM Song WHERE song_id = {id}')
            rows = cursor.fetchall()
            
            return {'statusCode': 200, "Message": "Song has been updated successfully", "body": json.dumps(rows[0])}
        except Exception as e:
            return {"Error": "In UPDATE " + str(e)}
    
    if path == "/deleteSong":
        #METHOD: DELETE

        id = event['queryStringParameters']['id']
        print(id)
        try:
            cursor.execute(f'DELETE FROM Song WHERE song_id={id}')
            
            #Commit to save changes
            connection.commit()
            return {"Message": "Song has been deleted successfully"}
        except Exception as e:
            return {"Error": "In DELETE " + str(e)}
    
