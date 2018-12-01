FROM jekyll/builder as builder
WORKDIR /build
COPY . .

RUN chown -R jekyll:jekyll /build \
    && jekyll build --destination targetdir --baseurl '/help' \
    && cd ../ \
    && find /build/targetdir -name *.md | xargs rm -f

FROM alpine
WORKDIR /root/
COPY --from=builder /build/targetdir .