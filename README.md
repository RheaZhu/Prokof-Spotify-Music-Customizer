# Prokof-Spotify-Music-Customizer
Prokof (pronounced "PRO-COUGHED") is a Spotify curator that customizes song recommendations based on your listening preferences. Implementing various coding languages and frameworks, Prokof is designed to be multi-functional, personalizable, yet still easy to use. 

## How Does Prokof Work?
Prokof uses a combination of Python, Flask, SQL, JavaScript, HTML, and CSS to curate music and generate its website. Importantly, this application incorporates Spotify’s Web Application Programming Interface (API), a library of functions enabling the integration of Spotify’s artist and music data into Prokof. The following procedure illustrates the rough method of executing Prokof's programming: 

1. Connect Prokof’s Flask web application with Spotify’s Web API. </li>
2. Given user server-side inputs into Prokof, request song metadata via the Spotify API. </li>
3. Search songs/albums with similar audio metadata. </li>
4. Output songs as a list onto the Prokof web application, along with a Spotify embed for each output. </li>
5. Use Spotify’s playlist Web API features to compile and output a playlist combining all recommended songs.

## Why Prokof?
Compared to other popular song generators, Prokof holds several advantages:
- Improved customizability: Unlike most others which only allow one song input, Prokof allows users to input multiple songs to personalize recommendations.
- Price: Prokof is free to use, with no hidden costs or subscriptions.
- Modifications: Prokof is open-source, allowing users to view and modify the code.

## How To Use Prokof
> Update: In November 2024, Spotify restricted public users' Web API use cases to a very limited collection of endpoints. As a result, Prokof has been forced to use the very limited data that Spotify still offers, which may result in slightly less functionality.
### STEP 1. Choose a Mode 
Prokof has three modes, each recommending a different number of songs based on your input: mode 1 recommends a maximum of 50 songs, mode 2 20 songs, and mode 3 10 songs. While all three modes use the same algorithm, their processing speeds differ; as expected, mode 1 is the slowest and mode 3 is the fastest. To choose a mode, click on the "Try Prok" button on the homepage, which will take you to the instructions page. From there, you can select your desired mode.
### STEP 2. Choose Your Songs 
Once you have chosen a mode, you will be redirected to a page to enter your inputs. You can input up to 5 songs, and for each selection, you should enter the song name and artist name in the respective fields. You do not have to input all 5 songs, but you must input at least one song. Note the following:
- Prokof will only accept song names and artist names that are in Spotify's database. If you input a song that is not in Spotify's database, Prokof will not be able to find it.
- Prokof will only accept song names and artist names that are spelled correctly. If you input a song or artist name with a typo, Prokof may not be able to find it.
- Prokof will only accept song names and artist names that are in English. If you input a song or artist name in another language, Prokof may not be able to find it.
### STEP 3. See Your Song Recommendations
After you have submitted your inputs, Prokof will process your request and generate a list of recommended songs based on your inputs. You will be redirected to a page that displays your recommendations, which will include the song name, artist name, and a Spotify embed for each song. You can listen to the songs directly from the page by clicking on the Spotify embed.
