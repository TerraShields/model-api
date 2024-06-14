## TerraShields Model API

### NOTE

- all url need Bearer token

### BASE URL

- https://api-model-tpercgplna-et.a.run.app

#### Post report with image

```http
  POST {{url}}/api/report
```

| Parameter   | Type             | Description   |
| :---------- | :--------------- | :------------ |
| `latitude`  | `string`         | **Required**. |
| `longitude` | `string`         | **Required**. |
| `sign`      | `string`         | **Required**. |
| `image`     | `jpg, jpeg, png` | **Required**. |

- success return body

```json
{
	"message": "success",
	"data": {
		"user_id": "user-2a35342b-2f66-46fc-b6b1-0dee64f0cac8",
		"report_id": "report-d3935ff0-f5ac-4c44-a06a-58f517a8428b",
		"created_at": "2024-06-14T22:19:26.232367Z",
		"delete_countdown": "2024-06-21T22:19:26.232367Z",
		"image": "",
		"sign": "sangat bahaya sekali gais",
		"description": "",
		"location": {
			"_latitude": 90.0,
			"_longitude": 180.0
		},
		"result": {
			"class": "bagaimana cara menanam padi yang baik dan benar",
			"probability": ""
		}
	}
}
```

- error return body

```json
{
	"error": "string"
}
```

#### Post report without image

```http
  POST {{url}}/api/report/capt
```

| Parameter   | Type     | Description   |
| :---------- | :------- | :------------ |
| `latitude`  | `string` | **Required**. |
| `longitude` | `string` | **Required**. |
| `sign`      | `string` | **Required**. |
| `caption`   | `string` | **Required**. |

- success return body

```json
{
	"message": "success",
	"data": {
		"user_id": "user-2a35342b-2f66-46fc-b6b1-0dee64f0cac8",
		"report_id": "report-d3935ff0-f5ac-4c44-a06a-58f517a8428b",
		"created_at": "2024-06-14T22:19:26.232367Z",
		"delete_countdown": "2024-06-21T22:19:26.232367Z",
		"image": "",
		"sign": "sangat bahaya sekali gais",
		"description": "",
		"location": {
			"_latitude": 90.0,
			"_longitude": 180.0
		},
		"result": {
			"class": "bagaimana cara menanam padi yang baik dan benar",
			"probability": ""
		}
	}
}
```

- error return body

```json
{
	"error": "string"
}
```

# IN DEVELOPMENT (i hate py)

#### Post Chat Bot

```http
  POST {{url}}/api/chat
```

| Parameter | Type     | Description   |
| :-------- | :------- | :------------ |
| `caption` | `string` | **Required**. |

- success return body

```json
{
	"system": "success"
}
```
