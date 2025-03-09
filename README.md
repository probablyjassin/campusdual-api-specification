# CampusDual API Specification

## Overview

The API allows students of (among others?) the Duale Hochschule Sachsen to access different pieces of information concerning their studying.

**Base URL**: `https://selfservice.campus-dual.de`  
**Format**: JSON  
**Version**: ?

## Status Codes

In general, the API returns `200 OK` regardless of success. If the request lacks proper authentication or anything else went wrong, the API returns this HTML-page:

```
Unbehandelter Fehler:

Zend_Controller_Exception

**Fehlermeldung:** Invalid controller specified (error)#0 /home/cdssp/www/library/Zend/Controller/Front.php(954): Zend_Controller_Dispatcher_Standard->dispatch(Object(Zend_Controller_Request_Http), Object(Zend_Controller_Response_Http)) #1 /home/cdssp/www/application/bootstrap.php(77): Zend_Controller_Front->dispatch() #2 /home/cdssp/www/public/index.php(2): require('/home/cdssp/www...') #3 {main}

```

## Authentication

Authentication happens via the query-parameters of the request, including the student identification number, and a hash which is likely a combination of the id number, account password and some salt.

## Obtaining the Hash

You will see your hash in the query parameters of requests to the API in your browser when using the website. Obtaining it only through scripting is more tedious.
The hash is obtainable by emulating a login to the site, but this cannot be done in the browser because of missing CORS. You would need a custom API to manage logins, bringing it's own security considerations for handling user credentials. Your hash is unlikely to change when your account password is not changing.
Check [here](https://github.com/Schrankian/campus-dual-app/issues/12#issuecomment-2399062382) and [here](https://github.com/probablyjassin/campusdual-api-specification/blob/main/hash.py) for instructions on how to do this.

## Rate Limiting

I have not encountered any rate limits while using this API. The website itself makes requests to the API in an inefficient manner, therefore rate limiting is likely not a concern for developers here.

## Endpoints

#### Student Current Semester

- **URL**: `/dash/getfs`
- **Method**: `GET`
- **Query Parameters for Auth**: `user`, `hash`

**Request**:

```text
https://selfservice.campus-dual.de/dash/getfs?user=<ID>&hash=<HASH>
```

**Response** (example):

```text
"02 "
```

(yes that whitespace is not a typo by me I don't know why it's there)

#### Student Credit Points

- **URL**: `/dash/getcp`
- **Method**: `GET`
- **Query Parameters for Auth**: `user`, `hash`

**Request**:

```text
https://selfservice.campus-dual.de/dash/getcp?user=<ID>&hash=<HASH>
```

**Response** (example):

```json
14
```

#### Student Timeline

- **URL**: `/dash/gettimeline`
- **Method**: `GET`
- **Query Parameters for Auth**: `user`, `hash`

**Request**:

```text
https://selfservice.campus-dual.de/dash/gettimeline?user=<ID>&hash=<HASH>
```

**Response** (example):

```json
{
	"wiki-url": "https://selfservice.campus-dual.de/dash/timeline",
	"wiki-section": "Campus-Dual Blockplan",
	"dateTimeFormat": "Gregorian",
	"events": [
		{
			"start": "Tue, 01 Oct 2024 00:00:00 +0200",
			"end": "Sun, 22 Dec 2024 00:00:00 +0100",
			"durationEvent": true,
			"color": "#0070a3",
			"title": "Theorie",
			"caption": "01.10.2024 bis 22.12.2024",
			"description": "<strong>Theoriephase</strong> 1. Fachsemester<br>vom 01.10.2024 bis 22.12.2024",
			"trackNum": 2
		},
		{
			"start": "Mon, 23 Dec 2024 00:00:00 +0100",
			"end": "Sun, 30 Mar 2025 00:00:00 +0100",
			"durationEvent": true,
			"color": "#119911",
			"title": "Praxis",
			"caption": "23.12.2024 bis 30.03.2025",
			"description": "<strong>Praxisphase</strong> 1. Fachsemester<br>vom 23.12.2024 bis 30.03.2025",
			"trackNum": 3
		}
	]
}
```

#### Student Exam Stats

- **URL**: `/dash/getexamstats`
- **Method**: `GET`
- **Query Parameters for Auth**: `user`, `hash`

**Request**:

```text
https://selfservice.campus-dual.de/dash/getexamstats?user=<ID>&hash=<HASH>
```

**Response** (example):

```json
{ "EXAMS": 4, "SUCCESS": 3, "FAILURE": 1, "WPCOUNT": 5, "MODULES": 3, "BOOKED": 0, "MBOOKED": 4 }
```

#### Student Timetable

- **URL**: `/room/json`
- **Method**: `GET`
- **Query Parameters for Auth**: `userid`, `hash`
- **Other Query Parameters:** `start`, `end`, `_`

**Fun fact**: The other last 3 parameters are broken and will have no influence on the response. They were likely meant to limit the size of the returned timetable to the appropriate scope, however the API always returns the entire student timetable available (which is likely part of why the response takes between 2 and 6 seconds).

**Another fun fact**: Notice how this and only this endpoint uses `userid` rather than `user`

**Hint**: Adding a parameter with the current unix-timestamp may still be advantageous to prevent caching, resulting in an outdated result if the timetable changed recently

**Request**:

```text
https://selfservice.campus-dual.de/room/json?userid=<ID>&hash=<HASH>
```

**Response** (example):

```json
[
	{
		"title": "5CS-ZSPLM-11",
		"start": 1727762400,
		"end": 1727767800,
		"allDay": false,
		"description": "Zentrales Stundenplanungsmodul",
		"color": "orange",
		"editable": false,
		"room": "205 Seminarraum",
		"sroom": "5SR 205",
		"instructor": "Prof. REDACTED",
		"sinstructor": "REDACTED",
		"remarks": "Einf\u00fchrung in das Studium durch die Studiengangleitung"
	},
	{
		"title": "5CS-ETHLE-10",
		"start": 1727769600,
		"end": 1727775000,
		"allDay": false,
		"description": "VS Grdl. d. Elektrot. u.Halbleiterel.",
		"color": "orange",
		"editable": false,
		"room": "205 Seminarraum",
		"sroom": "5SR 205",
		"instructor": "Prof. REDACTED",
		"sinstructor": "REDACTED",
		"remarks": ""
	}
]
```

# Q&A

**Q**: Why does the API always return `200 OK` even if the authentication went wrong? Isn't this wrong?

**A**: yes.

**Q**: Why does authentication happen over query-parameters instead of headers? Isn't this bad practice?

**A**: yes.

**Q**: Why is `room/json` so broken, resulting in it always sending the entire timetable and taking multiple seconds to load? Doesn't this suck?

**A**: yes.

**Q**: Why is `/room/json` the only endpoint that uses `userid` instead of `user` for auth like every other endpoint? Isn't this inconsistent?

**A**: yes
