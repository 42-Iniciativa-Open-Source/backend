# Middleman Backend

## Motivation

To use 42 API you need create an "Application" in your profile and generate an Bearer Token with Client ID and Cliet Secret provided to be able to make requests. So far so good, right? But Bearer Token provided just is valid for the first 7200 seconds (i.e 2 hours) and you only can perfom 1200 requests per hour. So you don't want to handle with this issues.

This project comes to solve this problem. Facilitate the use of the 42 API by managing tokens, bypassing the limit of requests by spreading through various applications and not letting other applications worry about what is not their responsibility.

## Usage

### Your own

You can deploy this project yourself with this [guide](DEPLOY.md).

### Host by us

Currently the project is deployed on [Heroku](https://www.heroku.com/). First, to access some endpoint, you need contact personally someone on the [project team](https://github.com/orgs/42-Iniciativa-Open-Source/people) and ask for a `Authorization` code.

Now you can perform a test request:

```bash
curl --request GET \
  --url https://iniciativa-open-source.herokuapp.com/42/users/csouza-f \
  --header 'Authorization: your_authorization'
```

That's it! This way you will get all information about user `csouza-f`.

The idea behind this is you pass any endpoint available by 42 after `https://iniciativa-open-source.herokuapp.com/42`. It's important to note that this endpoint make all requests already with `/v2`. For example, this `https://iniciativa-open-source.herokuapp.com/42/users/csouza-f` basically is `https://api.intra.42.fr/v2/users/csouza-f`.

[Here](https://api.intra.42.fr/apidoc) you can check all endpoints available.

#### Pagination

The amount of pages available for a endpoint is displayed on response headers. For example, `/apps` endpoint:

```bash
curl --request GET \
  --url https://iniciativa-open-source.herokuapp.com/42/apps \
  --header 'authorization: your_authorization'
```

When a request is performed, you can check out the response headers

![Response headers /apps](https://github.com/42-Iniciativa-Open-Source/backend/blob/media/apps.png)

As you can see the marked headers are the last, next and current page. So, you can paginated a endpoint using query string `page={page}` this way.
Maybe you want more data per request, so you can use `page[size]=100`, which is the maximum allowed from 42's API, default is 30. You can check out more on [42 API Docs](https://api.intra.42.fr/apidoc/guides/getting_started):

```bash
curl --request GET \
  --url https://iniciativa-open-source.herokuapp.com/42/apps?page[size]=100 \
  --header 'authorization: your_authorization'
```

As more objects per request, pages on response headers decrease:

![Response headers /apps?page(size)=100](https://github.com/42-Iniciativa-Open-Source/backend/blob/media/appssize100.png)

Or you can get all pages at once with special query string `page=all`. **This is in alpha and just available for /apps endpoint**.

```bash
curl --request GET \
  --url https://iniciativa-open-source.herokuapp.com/42/apps?page=all \
  --header 'authorization: your_authorization'
```

How this return all pages already, no one page header is set, but you will get all pages from `/apps` endpoint at once!

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPL v3](https://choosealicense.com/licenses/gpl-3.0/)

## Diagram

![Middleman diagram](https://github.com/42-Iniciativa-Open-Source/backend/blob/media/middleman.jpg)
