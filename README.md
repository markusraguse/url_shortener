# url_shortener

A simple URL shortening service built with Flask. This API allows users to shorten long URLs and redirect using shortened URLs

### Features
- **Shorten URL:** POST /shorten-url with {"url": "http://long-url.com"}. Receive {"url": "http://long-url.com", "short_url": "localhost:8080/abc123"}

- **Redirect:** GET /{short_code} to be redirected to the original URL.

### Documentation
Swagger documentation can be found by default at localhost:8080/apidocs
