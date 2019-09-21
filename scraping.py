from bs4 import BeautifulSoup as soup 
from urllib2 import urlopen
from selenium import webdriver
import time
import csv

def get_teams(url):
	teams = url.split("/")[-2].split("vs")
	home_team = home_team = teams[0][:-1]
	away_team = teams[1][1:]
	return [home_team,away_team]


def scrape_box(keyword,html):
	box_container = html.findAll("div", {"id" : keyword})
	box_divs = box_container[0].findAll("div", {"class" : "wwe-bar-chart-shadow"})
	box_home = str(box_divs[0].span.text)
	if box_home == "" :
		box_home = "0"
	box_away = str(box_divs[1].span.text)
	if box_away == "" :
		box_away = "0"
	return [box_home,box_away]

#creates the urls to the specific matches of match day match_day by reading in containers from the page
#the final urls to be scraped for stats are contained in match_urls
match_day = 1
url_name = "https://www.bundesliga.com/de/bundesliga/spieltag/2019-2020/" + str(match_day)

client = urlopen(url_name)
page_html = soup(client.read(), "html.parser")
client.close()

#probably put the data in a standardized dictionary with key = team_name
match_center_containers = page_html.findAll("a", {"class": "matchcenterLink"})
match_urls = []
for match_center_container in match_center_containers:
	full_match_info = str(match_center_container["href"]).split("/")
	match_info = full_match_info[-1]
	match_url = url_name + "/" + match_info + "/stats"
	match_urls.append(match_url)
match_urls = list(set(match_urls))

home_teams = []
away_teams = []
for url in match_urls :
	teams = get_teams(url)
	home_team = teams[0]
	away_team = teams[1]
	#need webbrowser to generate the javascript generated HTML 
	match_browser = webdriver.Firefox()
	match_browser.get(url)
	time.sleep(3)

	match_html = soup(match_browser.page_source, "html.parser")
	match_browser.quit()
	
	result_container = match_html.findAll("div", {"class" : "infos ng-star-inserted"})
	match_result = str(result_container[0].p.text)
	home_goals = str(match_result[0])
	away_goals = str(match_result[-1])
	result_indicators = []
	#if home_goals > away_goals :
	#	result_indicators = ["w", "l"]
	#elif home_goals < away_goals :
#		result_indicators = ["l", "w"]
#	else :
		#result_indicators = ["d", "d"]

	red_cards = scrape_box("wwe-data-red-cards", match_html)
	yellowred_cards = scrape_box("wwe-data-yellowred-cards", match_html)
	yellow_cards = scrape_box("wwe-data-yellow-cards", match_html)
	fouls = scrape_box("wwe-data-fouls", match_html)
	total_fouls = scrape_box("wwe-data-fairness-all", match_html)
	offsides = scrape_box("wwe-data-offsides", match_html)
	left_corners = scrape_box("wwe-data-corner-kicks-left", match_html)
	right_corners = scrape_box("wwe-data-corner-kicks-right", match_html)
	total_corners =  scrape_box("wwe-data-corner-kicks", match_html)
	total_headers_on_target = scrape_box("wwe-data-shots-total-header", match_html)
	total_attempts_on_target_inside_box = scrape_box("wwe-data-shots-total-inside-box", match_html)
	shots_on_target_inside_box = scrape_box("wwe-data-shots-foot-inside-box", match_html)
	total_attempts_on_target_outside_box = scrape_box("wwe-data-shots-total-outside-box", match_html)
	shots_on_target_outside_box = scrape_box("wwe-data-shots-foot-outside-box", match_html)
	total_attempts_on_target = scrape_box("wwe-data-shots-total", match_html)
	fraction_of_challenges_won = scrape_box("wwe-data-duels-won", match_html)
	number_of_successful_passes = scrape_box("wwe-data-passes-completed", match_html)
	fraction_of_successful_passes = scrape_box("wwe-data-passes-completed-percent", match_html)
	number_of_unsuccessful_passes = scrape_box("wwe-data-passes-failed", match_html)
	fraction_of_unsuccessful_passes = scrape_box("wwe-data-passes-failed-percent", match_html)
	number_of_possession_phases = scrape_box("wwe-data-balls-touched", match_html)
	fraction_of_possession_phases = scrape_box("wwe-data-balls-touched-percent", match_html)
	left_crosses = scrape_box("wwe-data-crosses-left", match_html)
	right_crosses = scrape_box("wwe-data-crosses-right" , match_html)
	total_crosses = scrape_box("wwe-data-crosses", match_html)
	distance_in_intensive_runs = scrape_box("wwe-data-tracking-intensive-runs-distance", match_html)
	distance_in_sprints = scrape_box("wwe-data-tracking-sprints-distance", match_html)
	distance_in_fast_runs = scrape_box("wwe-data-tracking-fast-runs-distance", match_html)
	number_of_intensive_runs = scrape_box("wwe-data-tracking-intensive-runs", match_html)
	number_of_sprints = scrape_box("wwe-data-tracking-sprints", match_html)
	number_of_fast_runs = scrape_box("wwe-data-tracking-fast-runs", match_html)
	total_distance = scrape_box("wwe-data-tracking-distance", match_html)
	average_speed = scrape_box("wwe-data-tracking-average-speed", match_html)


	home_goals_scored = home_goals
	home_goals_received = away_goals
	home_red_cards = red_cards[0]
	home_yellowred_cards = yellowred_cards[0]
	home_yellow_cards = yellow_cards[0]
	home_fouls = fouls[0]
	home_total_fouls = total_fouls[0]
	home_offsides = offsides[0]
	home_left_corners = left_corners[0]
	home_right_corners = right_corners[0]
	home_total_corners = total_corners[0] 
	home_total_headers_on_target = total_headers_on_target[0]
	home_total_attempts_on_target_inside_box = total_attempts_on_target_inside_box[0]
	home_shots_on_target_inside_box = shots_on_target_inside_box[0]
	home_total_attempts_on_target_outside_box = total_attempts_on_target_outside_box[0]
	home_shots_on_target_outside_box = shots_on_target_outside_box[0]
	home_total_attempts_on_target = total_attempts_on_target[0]
	home_fraction_of_challenges_won = fraction_of_challenges_won[0]
	home_number_of_successful_passes = number_of_successful_passes[0]
	home_fraction_of_successful_passes = fraction_of_successful_passes[0]
	home_number_of_unsuccessful_passes = number_of_unsuccessful_passes[0]
	home_fraction_of_unsuccessful_passes = fraction_of_unsuccessful_passes[0]
	home_number_of_possession_phases = number_of_possession_phases[0]
	home_fraction_of_possession_phases = fraction_of_possession_phases[0]
	home_left_crosses = left_crosses[0]
	home_right_crosses = right_crosses[0]
	home_total_crosses = total_crosses[0]
	home_distance_in_intensive_runs = distance_in_intensive_runs[0]
	home_distance_in_sprints = distance_in_sprints[0]
	home_distance_in_fast_runs = distance_in_fast_runs[0]
	home_number_of_intensive_runs = number_of_intensive_runs[0]
	home_number_of_sprints = number_of_sprints[0]
	home_number_of_fast_runs = number_of_fast_runs[0]
	home_total_distance = total_distance[0]
	home_average_speed = average_speed[0]

	away_goals_scored = away_goals
	away_goals_received = home_goals
	away_red_cards = red_cards[1]
	away_yellowred_cards = yellowred_cards[1]
	away_yellow_cards = yellow_cards[1]
	away_fouls = fouls[1]
	away_total_fouls = total_fouls[1]
	away_offsides = offsides[1]
	away_left_corners = left_corners[1]
	away_right_corners = right_corners[1]
	away_total_corners = total_corners[1] 
	away_total_headers_on_target = total_headers_on_target[1]
	away_total_attempts_on_target_inside_box = total_attempts_on_target_inside_box[1]
	away_shots_on_target_inside_box = shots_on_target_inside_box[1]
	away_total_attempts_on_target_outside_box = total_attempts_on_target_outside_box[1]
	away_shots_on_target_outside_box = shots_on_target_outside_box[1]
	away_total_attempts_on_target = total_attempts_on_target[1]
	away_fraction_of_challenges_won = fraction_of_challenges_won[1]
	away_number_of_successful_passes = number_of_successful_passes[1]
	away_fraction_of_successful_passes = fraction_of_successful_passes[1]
	away_number_of_unsuccessful_passes = number_of_unsuccessful_passes[1]
	away_fraction_of_unsuccessful_passes = fraction_of_unsuccessful_passes[1]
	away_number_of_possession_phases = number_of_possession_phases[1]
	away_fraction_of_possession_phases = fraction_of_possession_phases[1]
	away_left_crosses = left_crosses[1]
	away_right_crosses = right_crosses[1]
	away_total_crosses = total_crosses[1]
	away_distance_in_intensive_runs = distance_in_intensive_runs[1]
	away_distance_in_sprints = distance_in_sprints[1]
	away_distance_in_fast_runs = distance_in_fast_runs[1]
	away_number_of_intensive_runs = number_of_intensive_runs[1]
	away_number_of_sprints = number_of_sprints[1]
	away_number_of_fast_runs = number_of_fast_runs[1]
	away_total_distance = total_distance[1]
	away_average_speed = average_speed[1]

	#TODO:  -functionality to write to csv file without deleting previous data 
	#	    -possibility to input match_day variable from console when calling script

	with open(str(home_team)+".csv", mode="w") as home_file:
		home_writer = csv.writer(home_file, delimiter=",")
		home_writer.writerow([home_goals_scored,home_goals_received])

	with open(str(away_team)+".csv", mode="w") as away_file:
		away_writer = csv.writer(away_file, delimiter=",")
		away_writer.writerow([away_goals_scored,away_goals_received])



















#foul_container = match_html.findAll("div", {"id" : "wwe-data-fouls"})
#foul_divs = foul_container[0].findAll("div", {"class" : "wwe-bar-chart-shadow"})
#fouls_home = str(foul_divs[0].span.text)
#fouls_away = str(foul_divs[1].span.text)
#print "fouls home: " + fouls_home
#print "fouls away: " + fouls_away

#offside_container = match_html.findAll("div", {"id" : "wwe-data-offsides"})
#offside_divs = offside_container[0].findAll("div", {"class" : "wwe-bar-chart-shadow"})
#offsides_home = str(offside_divs[0].span.text)
#offsides_away = str(offside_divs[1].span.text)
#print "offsides home: " + offsides_home
#print "offsides away: " + offsides_away

#corner_container = match_html.findAll("div", {"id" : "wwe-data-corner-kicks-left"})
#corner_divs = corner_container[0].findAll("div", {"class" : "wwe-bar-chart-shadow"})
#corners_home = str(corner_divs[0].span.text)
#corners_away = str(corner_divs[1].span.text)
#if corners_away == "" :
#	corners_away = "0"
#print "corners home: " + corners_home
#print "corners away: " + corners_away
