function O(t) {
    return u(function (t) {
        for (var e = "", n = 0, r = Object.keys(t); n < r.length; n++) {
            var o = r[n]
                , i = t[o]
                , a = i.error ? "error" : JSON.stringify(i.value);
            e += (e ? "|" : "") + o.replace(/([:|\\])/g, "\\$1") + ":" + a
        }
        return e
    }(t))
}

function a(t, e) {
    return 32 === (e %= 64) ? [t[1], t[0]] : e < 32 ? [t[0] << e | t[1] >>> 32 - e, t[1] << e | t[0] >>> 32 - e] : (e -= 32,
        [t[1] << e | t[0] >>> 32 - e, t[0] << e | t[1] >>> 32 - e])
}

function i(t, e) {
    t = [t[0] >>> 16, 65535 & t[0], t[1] >>> 16, 65535 & t[1]],
        e = [e[0] >>> 16, 65535 & e[0], e[1] >>> 16, 65535 & e[1]];
    var n = [0, 0, 0, 0];
    return n[3] += t[3] * e[3],
        n[2] += n[3] >>> 16,
        n[3] &= 65535,
        n[2] += t[2] * e[3],
        n[1] += n[2] >>> 16,
        n[2] &= 65535,
        n[2] += t[3] * e[2],
        n[1] += n[2] >>> 16,
        n[2] &= 65535,
        n[1] += t[1] * e[3],
        n[0] += n[1] >>> 16,
        n[1] &= 65535,
        n[1] += t[2] * e[2],
        n[0] += n[1] >>> 16,
        n[1] &= 65535,
        n[1] += t[3] * e[1],
        n[0] += n[1] >>> 16,
        n[1] &= 65535,
        n[0] += t[0] * e[3] + t[1] * e[2] + t[2] * e[1] + t[3] * e[0],
        n[0] &= 65535,
        [n[0] << 16 | n[1], n[2] << 16 | n[3]]
}

function o(t, e) {
    t = [t[0] >>> 16, 65535 & t[0], t[1] >>> 16, 65535 & t[1]],
        e = [e[0] >>> 16, 65535 & e[0], e[1] >>> 16, 65535 & e[1]];
    var n = [0, 0, 0, 0];
    return n[3] += t[3] + e[3],
        n[2] += n[3] >>> 16,
        n[3] &= 65535,
        n[2] += t[2] + e[2],
        n[1] += n[2] >>> 16,
        n[2] &= 65535,
        n[1] += t[1] + e[1],
        n[0] += n[1] >>> 16,
        n[1] &= 65535,
        n[0] += t[0] + e[0],
        n[0] &= 65535,
        [n[0] << 16 | n[1], n[2] << 16 | n[3]]
}

function u(t, e) {
    e = e || 0;
    var n, r = (t = t || "").length % 16, u = t.length - r, f = [0, e], d = [0, e], h = [0, 0], p = [0, 0],
        v = [2277735313, 289559509], m = [1291169091, 658871167];
    for (n = 0; n < u; n += 16)
        h = [255 & t.charCodeAt(n + 4) | (255 & t.charCodeAt(n + 5)) << 8 | (255 & t.charCodeAt(n + 6)) << 16 | (255 & t.charCodeAt(n + 7)) << 24, 255 & t.charCodeAt(n) | (255 & t.charCodeAt(n + 1)) << 8 | (255 & t.charCodeAt(n + 2)) << 16 | (255 & t.charCodeAt(n + 3)) << 24],
            p = [255 & t.charCodeAt(n + 12) | (255 & t.charCodeAt(n + 13)) << 8 | (255 & t.charCodeAt(n + 14)) << 16 | (255 & t.charCodeAt(n + 15)) << 24, 255 & t.charCodeAt(n + 8) | (255 & t.charCodeAt(n + 9)) << 8 | (255 & t.charCodeAt(n + 10)) << 16 | (255 & t.charCodeAt(n + 11)) << 24],
            h = a(h = i(h, v), 31),
            f = o(f = a(f = c(f, h = i(h, m)), 27), d),
            f = o(i(f, [0, 5]), [0, 1390208809]),
            p = a(p = i(p, m), 33),
            d = o(d = a(d = c(d, p = i(p, v)), 31), f),
            d = o(i(d, [0, 5]), [0, 944331445]);
    switch (h = [0, 0],
        p = [0, 0],
        r) {
        case 15:
            p = c(p, s([0, t.charCodeAt(n + 14)], 48));
        case 14:
            p = c(p, s([0, t.charCodeAt(n + 13)], 40));
        case 13:
            p = c(p, s([0, t.charCodeAt(n + 12)], 32));
        case 12:
            p = c(p, s([0, t.charCodeAt(n + 11)], 24));
        case 11:
            p = c(p, s([0, t.charCodeAt(n + 10)], 16));
        case 10:
            p = c(p, s([0, t.charCodeAt(n + 9)], 8));
        case 9:
            p = i(p = c(p, [0, t.charCodeAt(n + 8)]), m),
                d = c(d, p = i(p = a(p, 33), v));
        case 8:
            h = c(h, s([0, t.charCodeAt(n + 7)], 56));
        case 7:
            h = c(h, s([0, t.charCodeAt(n + 6)], 48));
        case 6:
            h = c(h, s([0, t.charCodeAt(n + 5)], 40));
        case 5:
            h = c(h, s([0, t.charCodeAt(n + 4)], 32));
        case 4:
            h = c(h, s([0, t.charCodeAt(n + 3)], 24));
        case 3:
            h = c(h, s([0, t.charCodeAt(n + 2)], 16));
        case 2:
            h = c(h, s([0, t.charCodeAt(n + 1)], 8));
        case 1:
            h = i(h = c(h, [0, t.charCodeAt(n)]), v),
                f = c(f, h = i(h = a(h, 31), m))
    }
    return f = o(f = c(f, [0, t.length]), d = c(d, [0, t.length])),
        d = o(d, f),
        f = o(f = l(f), d = l(d)),
        d = o(d, f),
    ("00000000" + (f[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (f[1] >>> 0).toString(16)).slice(-8) + ("00000000" + (d[0] >>> 0).toString(16)).slice(-8) + ("00000000" + (d[1] >>> 0).toString(16)).slice(-8)
}

function c(t, e) {
    return [t[0] ^ e[0], t[1] ^ e[1]]
}

function s(t, e) {
    return 0 === (e %= 64) ? t : e < 32 ? [t[0] << e | t[1] >>> 32 - e, t[1] << e] : [t[1] << e - 32, 0]
}

function l(t) {
    return t = c(t, [0, t[0] >>> 1]),
        t = c(t = i(t, [4283543511, 3981806797]), [0, t[0] >>> 1]),
        t = c(t = i(t, [3301882366, 444984403]), [0, t[0] >>> 1])
}