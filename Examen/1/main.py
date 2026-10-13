from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
    SITES
)

print("\n PARTEA 1 ")
print("URL fara slash:", build_url("example.com", "login"))
print("URL cu slash:", build_url("example.com", "/login"))
print("HTTPS:", is_https("https://example.com"))
print("HTTP:", is_https("http://example.com"))

print("\n PARTEA 2 ")
show_response("https://example.com")
show_response("http://this-site-does-not-exist.invalid")

print("\n PARTEA 3")
print("Site functional:", check_site("https://example.com"))
print("Site inexistent:", check_site(
    "http://this-site-does-not-exist.invalid"
))

for url in SITES:
    print(url, "->", check_site(url))

print("\n PARTEA 4")
scan_sites()

print("\n PARTEA 5")
print(check_headers(
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"
))
print(check_headers("https://example.com"))
print(check_headers(
    "http://this-site-does-not-exist.invalid"
))

print("\n PARTEA 6")
print("Status 200:", retry_check("https://httpbin.org/status/200"))
print("Status 404:", retry_check("https://httpbin.org/status/404"))
print("Status 500:", retry_check("https://httpbin.org/status/500"))
print("Site inexistent:", retry_check(
    "http://this-site-does-not-exist.invalid"
))