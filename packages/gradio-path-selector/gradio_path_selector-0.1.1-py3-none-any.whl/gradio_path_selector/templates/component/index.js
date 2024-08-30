const {
  SvelteComponent: Jl,
  assign: Ql,
  create_slot: xl,
  detach: $l,
  element: ei,
  get_all_dirty_from_scope: ti,
  get_slot_changes: ni,
  get_spread_update: li,
  init: ii,
  insert: oi,
  safe_not_equal: si,
  set_dynamic_element_data: Mn,
  set_style: le,
  toggle_class: Te,
  transition_in: yl,
  transition_out: Al,
  update_slot_base: ai
} = window.__gradio__svelte__internal;
function ri(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), o = xl(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], f = {};
  for (let s = 0; s < a.length; s += 1)
    f = Ql(f, a[s]);
  return {
    c() {
      e = ei(
        /*tag*/
        l[14]
      ), o && o.c(), Mn(
        /*tag*/
        l[14]
      )(e, f), Te(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), Te(
        e,
        "padded",
        /*padding*/
        l[6]
      ), Te(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), Te(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), Te(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), le(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), le(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), le(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), le(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), le(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), le(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), le(e, "border-width", "var(--block-border-width)");
    },
    m(s, r) {
      oi(s, e, r), o && o.m(e, null), n = !0;
    },
    p(s, r) {
      o && o.p && (!n || r & /*$$scope*/
      131072) && ai(
        o,
        i,
        s,
        /*$$scope*/
        s[17],
        n ? ni(
          i,
          /*$$scope*/
          s[17],
          r,
          null
        ) : ti(
          /*$$scope*/
          s[17]
        ),
        null
      ), Mn(
        /*tag*/
        s[14]
      )(e, f = li(a, [
        (!n || r & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!n || r & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!n || r & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), Te(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), Te(
        e,
        "padded",
        /*padding*/
        s[6]
      ), Te(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), Te(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), Te(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), r & /*height*/
      1 && le(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), r & /*width*/
      2 && le(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), r & /*variant*/
      16 && le(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), r & /*allow_overflow*/
      2048 && le(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), r & /*scale*/
      4096 && le(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), r & /*min_width*/
      8192 && le(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      n || (yl(o, s), n = !0);
    },
    o(s) {
      Al(o, s), n = !1;
    },
    d(s) {
      s && $l(e), o && o.d(s);
    }
  };
}
function fi(l) {
  let e, t = (
    /*tag*/
    l[14] && ri(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (yl(t, n), e = !0);
    },
    o(n) {
      Al(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function ci(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: a = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: s = [] } = e, { variant: r = "solid" } = e, { border_mode: u = "base" } = e, { padding: d = !0 } = e, { type: E = "normal" } = e, { test_id: g = void 0 } = e, { explicit_call: A = !1 } = e, { container: D = !0 } = e, { visible: R = !0 } = e, { allow_overflow: U = !0 } = e, { scale: p = null } = e, { min_width: h = 0 } = e, k = E === "fieldset" ? "fieldset" : "div";
  const I = (w) => {
    if (w !== void 0) {
      if (typeof w == "number")
        return w + "px";
      if (typeof w == "string")
        return w;
    }
  };
  return l.$$set = (w) => {
    "height" in w && t(0, o = w.height), "width" in w && t(1, a = w.width), "elem_id" in w && t(2, f = w.elem_id), "elem_classes" in w && t(3, s = w.elem_classes), "variant" in w && t(4, r = w.variant), "border_mode" in w && t(5, u = w.border_mode), "padding" in w && t(6, d = w.padding), "type" in w && t(16, E = w.type), "test_id" in w && t(7, g = w.test_id), "explicit_call" in w && t(8, A = w.explicit_call), "container" in w && t(9, D = w.container), "visible" in w && t(10, R = w.visible), "allow_overflow" in w && t(11, U = w.allow_overflow), "scale" in w && t(12, p = w.scale), "min_width" in w && t(13, h = w.min_width), "$$scope" in w && t(17, i = w.$$scope);
  }, [
    o,
    a,
    f,
    s,
    r,
    u,
    d,
    g,
    A,
    D,
    R,
    U,
    p,
    h,
    k,
    I,
    E,
    i,
    n
  ];
}
class ui extends Jl {
  constructor(e) {
    super(), ii(this, e, ci, fi, si, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: _i,
  attr: di,
  create_slot: mi,
  detach: pi,
  element: hi,
  get_all_dirty_from_scope: gi,
  get_slot_changes: bi,
  init: wi,
  insert: Ti,
  safe_not_equal: Ei,
  transition_in: yi,
  transition_out: Ai,
  update_slot_base: ki
} = window.__gradio__svelte__internal;
function vi(l) {
  let e, t;
  const n = (
    /*#slots*/
    l[1].default
  ), i = mi(
    n,
    l,
    /*$$scope*/
    l[0],
    null
  );
  return {
    c() {
      e = hi("div"), i && i.c(), di(e, "class", "svelte-1hnfib2");
    },
    m(o, a) {
      Ti(o, e, a), i && i.m(e, null), t = !0;
    },
    p(o, [a]) {
      i && i.p && (!t || a & /*$$scope*/
      1) && ki(
        i,
        n,
        o,
        /*$$scope*/
        o[0],
        t ? bi(
          n,
          /*$$scope*/
          o[0],
          a,
          null
        ) : gi(
          /*$$scope*/
          o[0]
        ),
        null
      );
    },
    i(o) {
      t || (yi(i, o), t = !0);
    },
    o(o) {
      Ai(i, o), t = !1;
    },
    d(o) {
      o && pi(e), i && i.d(o);
    }
  };
}
function Si(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e;
  return l.$$set = (o) => {
    "$$scope" in o && t(0, i = o.$$scope);
  }, [i, n];
}
class Li extends _i {
  constructor(e) {
    super(), wi(this, e, Si, vi, Ei, {});
  }
}
const {
  SvelteComponent: Ci,
  attr: Dn,
  check_outros: Ri,
  create_component: Ni,
  create_slot: Oi,
  destroy_component: Mi,
  detach: Mt,
  element: Di,
  empty: Ii,
  get_all_dirty_from_scope: Pi,
  get_slot_changes: Fi,
  group_outros: Ui,
  init: zi,
  insert: Dt,
  mount_component: Hi,
  safe_not_equal: Bi,
  set_data: Gi,
  space: Wi,
  text: qi,
  toggle_class: xe,
  transition_in: ht,
  transition_out: It,
  update_slot_base: Vi
} = window.__gradio__svelte__internal;
function In(l) {
  let e, t;
  return e = new Li({
    props: {
      $$slots: { default: [Yi] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ni(e.$$.fragment);
    },
    m(n, i) {
      Hi(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*$$scope, info*/
      10 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (ht(e.$$.fragment, n), t = !0);
    },
    o(n) {
      It(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Mi(e, n);
    }
  };
}
function Yi(l) {
  let e;
  return {
    c() {
      e = qi(
        /*info*/
        l[1]
      );
    },
    m(t, n) {
      Dt(t, e, n);
    },
    p(t, n) {
      n & /*info*/
      2 && Gi(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Mt(e);
    }
  };
}
function ji(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[2].default
  ), a = Oi(
    o,
    l,
    /*$$scope*/
    l[3],
    null
  );
  let f = (
    /*info*/
    l[1] && In(l)
  );
  return {
    c() {
      e = Di("span"), a && a.c(), t = Wi(), f && f.c(), n = Ii(), Dn(e, "data-testid", "block-info"), Dn(e, "class", "svelte-22c38v"), xe(e, "sr-only", !/*show_label*/
      l[0]), xe(e, "hide", !/*show_label*/
      l[0]), xe(
        e,
        "has-info",
        /*info*/
        l[1] != null
      );
    },
    m(s, r) {
      Dt(s, e, r), a && a.m(e, null), Dt(s, t, r), f && f.m(s, r), Dt(s, n, r), i = !0;
    },
    p(s, [r]) {
      a && a.p && (!i || r & /*$$scope*/
      8) && Vi(
        a,
        o,
        s,
        /*$$scope*/
        s[3],
        i ? Fi(
          o,
          /*$$scope*/
          s[3],
          r,
          null
        ) : Pi(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || r & /*show_label*/
      1) && xe(e, "sr-only", !/*show_label*/
      s[0]), (!i || r & /*show_label*/
      1) && xe(e, "hide", !/*show_label*/
      s[0]), (!i || r & /*info*/
      2) && xe(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? f ? (f.p(s, r), r & /*info*/
      2 && ht(f, 1)) : (f = In(s), f.c(), ht(f, 1), f.m(n.parentNode, n)) : f && (Ui(), It(f, 1, 1, () => {
        f = null;
      }), Ri());
    },
    i(s) {
      i || (ht(a, s), ht(f), i = !0);
    },
    o(s) {
      It(a, s), It(f), i = !1;
    },
    d(s) {
      s && (Mt(e), Mt(t), Mt(n)), a && a.d(s), f && f.d(s);
    }
  };
}
function Zi(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { show_label: o = !0 } = e, { info: a = void 0 } = e;
  return l.$$set = (f) => {
    "show_label" in f && t(0, o = f.show_label), "info" in f && t(1, a = f.info), "$$scope" in f && t(3, i = f.$$scope);
  }, [o, a, n, i];
}
class Xi extends Ci {
  constructor(e) {
    super(), zi(this, e, Zi, ji, Bi, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Ki,
  append: xt,
  attr: Ne,
  bubble: Ji,
  create_component: Qi,
  destroy_component: xi,
  detach: kl,
  element: $t,
  init: $i,
  insert: vl,
  listen: eo,
  mount_component: to,
  safe_not_equal: no,
  set_data: lo,
  set_style: $e,
  space: io,
  text: oo,
  toggle_class: ne,
  transition_in: so,
  transition_out: ao
} = window.__gradio__svelte__internal;
function Pn(l) {
  let e, t;
  return {
    c() {
      e = $t("span"), t = oo(
        /*label*/
        l[1]
      ), Ne(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      vl(n, e, i), xt(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && lo(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && kl(e);
    }
  };
}
function ro(l) {
  let e, t, n, i, o, a, f, s = (
    /*show_label*/
    l[2] && Pn(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = $t("button"), s && s.c(), t = io(), n = $t("div"), Qi(i.$$.fragment), Ne(n, "class", "svelte-1lrphxw"), ne(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), ne(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), ne(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], Ne(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), Ne(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), Ne(
        e,
        "title",
        /*label*/
        l[1]
      ), Ne(e, "class", "svelte-1lrphxw"), ne(
        e,
        "pending",
        /*pending*/
        l[3]
      ), ne(
        e,
        "padded",
        /*padded*/
        l[5]
      ), ne(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), ne(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), $e(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), $e(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), $e(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(r, u) {
      vl(r, e, u), s && s.m(e, null), xt(e, t), xt(e, n), to(i, n, null), o = !0, a || (f = eo(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), a = !0);
    },
    p(r, [u]) {
      /*show_label*/
      r[2] ? s ? s.p(r, u) : (s = Pn(r), s.c(), s.m(e, t)) : s && (s.d(1), s = null), (!o || u & /*size*/
      16) && ne(
        n,
        "small",
        /*size*/
        r[4] === "small"
      ), (!o || u & /*size*/
      16) && ne(
        n,
        "large",
        /*size*/
        r[4] === "large"
      ), (!o || u & /*size*/
      16) && ne(
        n,
        "medium",
        /*size*/
        r[4] === "medium"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      r[7]), (!o || u & /*label*/
      2) && Ne(
        e,
        "aria-label",
        /*label*/
        r[1]
      ), (!o || u & /*hasPopup*/
      256) && Ne(
        e,
        "aria-haspopup",
        /*hasPopup*/
        r[8]
      ), (!o || u & /*label*/
      2) && Ne(
        e,
        "title",
        /*label*/
        r[1]
      ), (!o || u & /*pending*/
      8) && ne(
        e,
        "pending",
        /*pending*/
        r[3]
      ), (!o || u & /*padded*/
      32) && ne(
        e,
        "padded",
        /*padded*/
        r[5]
      ), (!o || u & /*highlight*/
      64) && ne(
        e,
        "highlight",
        /*highlight*/
        r[6]
      ), (!o || u & /*transparent*/
      512) && ne(
        e,
        "transparent",
        /*transparent*/
        r[9]
      ), u & /*disabled, _color*/
      4224 && $e(e, "color", !/*disabled*/
      r[7] && /*_color*/
      r[12] ? (
        /*_color*/
        r[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && $e(e, "--bg-color", /*disabled*/
      r[7] ? "auto" : (
        /*background*/
        r[10]
      )), u & /*offset*/
      2048 && $e(
        e,
        "margin-left",
        /*offset*/
        r[11] + "px"
      );
    },
    i(r) {
      o || (so(i.$$.fragment, r), o = !0);
    },
    o(r) {
      ao(i.$$.fragment, r), o = !1;
    },
    d(r) {
      r && kl(e), s && s.d(), xi(i), a = !1, f();
    }
  };
}
function fo(l, e, t) {
  let n, { Icon: i } = e, { label: o = "" } = e, { show_label: a = !1 } = e, { pending: f = !1 } = e, { size: s = "small" } = e, { padded: r = !0 } = e, { highlight: u = !1 } = e, { disabled: d = !1 } = e, { hasPopup: E = !1 } = e, { color: g = "var(--block-label-text-color)" } = e, { transparent: A = !1 } = e, { background: D = "var(--background-fill-primary)" } = e, { offset: R = 0 } = e;
  function U(p) {
    Ji.call(this, l, p);
  }
  return l.$$set = (p) => {
    "Icon" in p && t(0, i = p.Icon), "label" in p && t(1, o = p.label), "show_label" in p && t(2, a = p.show_label), "pending" in p && t(3, f = p.pending), "size" in p && t(4, s = p.size), "padded" in p && t(5, r = p.padded), "highlight" in p && t(6, u = p.highlight), "disabled" in p && t(7, d = p.disabled), "hasPopup" in p && t(8, E = p.hasPopup), "color" in p && t(13, g = p.color), "transparent" in p && t(9, A = p.transparent), "background" in p && t(10, D = p.background), "offset" in p && t(11, R = p.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : g);
  }, [
    i,
    o,
    a,
    f,
    s,
    r,
    u,
    d,
    E,
    A,
    D,
    R,
    n,
    g,
    U
  ];
}
class co extends Ki {
  constructor(e) {
    super(), $i(this, e, fo, ro, no, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: uo,
  append: Vt,
  attr: ue,
  detach: _o,
  init: mo,
  insert: po,
  noop: Yt,
  safe_not_equal: ho,
  set_style: Ee,
  svg_element: St
} = window.__gradio__svelte__internal;
function go(l) {
  let e, t, n, i;
  return {
    c() {
      e = St("svg"), t = St("g"), n = St("path"), i = St("path"), ue(n, "d", "M18,6L6.087,17.913"), Ee(n, "fill", "none"), Ee(n, "fill-rule", "nonzero"), Ee(n, "stroke-width", "2px"), ue(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), ue(i, "d", "M4.364,4.364L19.636,19.636"), Ee(i, "fill", "none"), Ee(i, "fill-rule", "nonzero"), Ee(i, "stroke-width", "2px"), ue(e, "width", "100%"), ue(e, "height", "100%"), ue(e, "viewBox", "0 0 24 24"), ue(e, "version", "1.1"), ue(e, "xmlns", "http://www.w3.org/2000/svg"), ue(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), ue(e, "xml:space", "preserve"), ue(e, "stroke", "currentColor"), Ee(e, "fill-rule", "evenodd"), Ee(e, "clip-rule", "evenodd"), Ee(e, "stroke-linecap", "round"), Ee(e, "stroke-linejoin", "round");
    },
    m(o, a) {
      po(o, e, a), Vt(e, t), Vt(t, n), Vt(e, i);
    },
    p: Yt,
    i: Yt,
    o: Yt,
    d(o) {
      o && _o(e);
    }
  };
}
class bo extends uo {
  constructor(e) {
    super(), mo(this, e, null, go, ho, {});
  }
}
const wo = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Fn = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
wo.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: Fn[e][t],
      secondary: Fn[e][n]
    }
  }),
  {}
);
function tt(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function Pt() {
}
function To(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Sl = typeof window < "u";
let Un = Sl ? () => window.performance.now() : () => Date.now(), Ll = Sl ? (l) => requestAnimationFrame(l) : Pt;
const lt = /* @__PURE__ */ new Set();
function Cl(l) {
  lt.forEach((e) => {
    e.c(l) || (lt.delete(e), e.f());
  }), lt.size !== 0 && Ll(Cl);
}
function Eo(l) {
  let e;
  return lt.size === 0 && Ll(Cl), {
    promise: new Promise((t) => {
      lt.add(e = { c: l, f: t });
    }),
    abort() {
      lt.delete(e);
    }
  };
}
const et = [];
function yo(l, e = Pt) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (To(l, f) && (l = f, t)) {
      const s = !et.length;
      for (const r of n)
        r[1](), et.push(r, l);
      if (s) {
        for (let r = 0; r < et.length; r += 2)
          et[r][0](et[r + 1]);
        et.length = 0;
      }
    }
  }
  function o(f) {
    i(f(l));
  }
  function a(f, s = Pt) {
    const r = [f, s];
    return n.add(r), n.size === 1 && (t = e(i, o) || Pt), f(l), () => {
      n.delete(r), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: a };
}
function zn(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function en(l, e, t, n) {
  if (typeof t == "number" || zn(t)) {
    const i = n - t, o = (t - e) / (l.dt || 1 / 60), a = l.opts.stiffness * i, f = l.opts.damping * o, s = (a - f) * l.inv_mass, r = (o + s) * l.dt;
    return Math.abs(r) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, zn(t) ? new Date(t.getTime() + r) : t + r);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => en(l, e[o], t[o], n[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = en(l, e[o], t[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Hn(l, e = {}) {
  const t = yo(l), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let a, f, s, r = l, u = l, d = 1, E = 0, g = !1;
  function A(R, U = {}) {
    u = R;
    const p = s = {};
    return l == null || U.hard || D.stiffness >= 1 && D.damping >= 1 ? (g = !0, a = Un(), r = R, t.set(l = u), Promise.resolve()) : (U.soft && (E = 1 / ((U.soft === !0 ? 0.5 : +U.soft) * 60), d = 0), f || (a = Un(), g = !1, f = Eo((h) => {
      if (g)
        return g = !1, f = null, !1;
      d = Math.min(d + E, 1);
      const k = {
        inv_mass: d,
        opts: D,
        settled: !0,
        dt: (h - a) * 60 / 1e3
      }, I = en(k, r, l, u);
      return a = h, r = l, t.set(l = I), k.settled && (f = null), !k.settled;
    })), new Promise((h) => {
      f.promise.then(() => {
        p === s && h();
      });
    }));
  }
  const D = {
    set: A,
    update: (R, U) => A(R(u, l), U),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return D;
}
const {
  SvelteComponent: Ao,
  append: _e,
  attr: M,
  component_subscribe: Bn,
  detach: ko,
  element: vo,
  init: So,
  insert: Lo,
  noop: Gn,
  safe_not_equal: Co,
  set_style: Lt,
  svg_element: de,
  toggle_class: Wn
} = window.__gradio__svelte__internal, { onMount: Ro } = window.__gradio__svelte__internal;
function No(l) {
  let e, t, n, i, o, a, f, s, r, u, d, E;
  return {
    c() {
      e = vo("div"), t = de("svg"), n = de("g"), i = de("path"), o = de("path"), a = de("path"), f = de("path"), s = de("g"), r = de("path"), u = de("path"), d = de("path"), E = de("path"), M(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), M(i, "fill", "#FF7C00"), M(i, "fill-opacity", "0.4"), M(i, "class", "svelte-43sxxs"), M(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), M(o, "fill", "#FF7C00"), M(o, "class", "svelte-43sxxs"), M(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), M(a, "fill", "#FF7C00"), M(a, "fill-opacity", "0.4"), M(a, "class", "svelte-43sxxs"), M(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), M(f, "fill", "#FF7C00"), M(f, "class", "svelte-43sxxs"), Lt(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), M(r, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), M(r, "fill", "#FF7C00"), M(r, "fill-opacity", "0.4"), M(r, "class", "svelte-43sxxs"), M(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), M(u, "fill", "#FF7C00"), M(u, "class", "svelte-43sxxs"), M(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), M(d, "fill", "#FF7C00"), M(d, "fill-opacity", "0.4"), M(d, "class", "svelte-43sxxs"), M(E, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), M(E, "fill", "#FF7C00"), M(E, "class", "svelte-43sxxs"), Lt(s, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), M(t, "viewBox", "-1200 -1200 3000 3000"), M(t, "fill", "none"), M(t, "xmlns", "http://www.w3.org/2000/svg"), M(t, "class", "svelte-43sxxs"), M(e, "class", "svelte-43sxxs"), Wn(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(g, A) {
      Lo(g, e, A), _e(e, t), _e(t, n), _e(n, i), _e(n, o), _e(n, a), _e(n, f), _e(t, s), _e(s, r), _e(s, u), _e(s, d), _e(s, E);
    },
    p(g, [A]) {
      A & /*$top*/
      2 && Lt(n, "transform", "translate(" + /*$top*/
      g[1][0] + "px, " + /*$top*/
      g[1][1] + "px)"), A & /*$bottom*/
      4 && Lt(s, "transform", "translate(" + /*$bottom*/
      g[2][0] + "px, " + /*$bottom*/
      g[2][1] + "px)"), A & /*margin*/
      1 && Wn(
        e,
        "margin",
        /*margin*/
        g[0]
      );
    },
    i: Gn,
    o: Gn,
    d(g) {
      g && ko(e);
    }
  };
}
function Oo(l, e, t) {
  let n, i;
  var o = this && this.__awaiter || function(g, A, D, R) {
    function U(p) {
      return p instanceof D ? p : new D(function(h) {
        h(p);
      });
    }
    return new (D || (D = Promise))(function(p, h) {
      function k(Y) {
        try {
          w(R.next(Y));
        } catch (K) {
          h(K);
        }
      }
      function I(Y) {
        try {
          w(R.throw(Y));
        } catch (K) {
          h(K);
        }
      }
      function w(Y) {
        Y.done ? p(Y.value) : U(Y.value).then(k, I);
      }
      w((R = R.apply(g, A || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const f = Hn([0, 0]);
  Bn(l, f, (g) => t(1, n = g));
  const s = Hn([0, 0]);
  Bn(l, s, (g) => t(2, i = g));
  let r;
  function u() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 140]), s.set([-125, -140])]), yield Promise.all([f.set([-125, 140]), s.set([125, -140])]), yield Promise.all([f.set([-125, 0]), s.set([125, -0])]), yield Promise.all([f.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function d() {
    return o(this, void 0, void 0, function* () {
      yield u(), r || d();
    });
  }
  function E() {
    return o(this, void 0, void 0, function* () {
      yield Promise.all([f.set([125, 0]), s.set([-125, 0])]), d();
    });
  }
  return Ro(() => (E(), () => r = !0)), l.$$set = (g) => {
    "margin" in g && t(0, a = g.margin);
  }, [a, n, i, f, s];
}
class Mo extends Ao {
  constructor(e) {
    super(), So(this, e, Oo, No, Co, { margin: 0 });
  }
}
const {
  SvelteComponent: Do,
  append: Ve,
  attr: he,
  binding_callbacks: qn,
  check_outros: tn,
  create_component: Rl,
  create_slot: Nl,
  destroy_component: Ol,
  destroy_each: Ml,
  detach: S,
  element: ve,
  empty: it,
  ensure_array_like: Ut,
  get_all_dirty_from_scope: Dl,
  get_slot_changes: Il,
  group_outros: nn,
  init: Io,
  insert: L,
  mount_component: Pl,
  noop: ln,
  safe_not_equal: Po,
  set_data: ae,
  set_style: ze,
  space: se,
  text: V,
  toggle_class: oe,
  transition_in: pe,
  transition_out: Se,
  update_slot_base: Fl
} = window.__gradio__svelte__internal, { tick: Fo } = window.__gradio__svelte__internal, { onDestroy: Uo } = window.__gradio__svelte__internal, { createEventDispatcher: zo } = window.__gradio__svelte__internal, Ho = (l) => ({}), Vn = (l) => ({}), Bo = (l) => ({}), Yn = (l) => ({});
function jn(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n[43] = t, n;
}
function Zn(l, e, t) {
  const n = l.slice();
  return n[41] = e[t], n;
}
function Go(l) {
  let e, t, n, i, o = (
    /*i18n*/
    l[1]("common.error") + ""
  ), a, f, s;
  t = new co({
    props: {
      Icon: bo,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const r = (
    /*#slots*/
    l[30].error
  ), u = Nl(
    r,
    l,
    /*$$scope*/
    l[29],
    Vn
  );
  return {
    c() {
      e = ve("div"), Rl(t.$$.fragment), n = se(), i = ve("span"), a = V(o), f = se(), u && u.c(), he(e, "class", "clear-status svelte-v0wucf"), he(i, "class", "error svelte-v0wucf");
    },
    m(d, E) {
      L(d, e, E), Pl(t, e, null), L(d, n, E), L(d, i, E), Ve(i, a), L(d, f, E), u && u.m(d, E), s = !0;
    },
    p(d, E) {
      const g = {};
      E[0] & /*i18n*/
      2 && (g.label = /*i18n*/
      d[1]("common.clear")), t.$set(g), (!s || E[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      d[1]("common.error") + "") && ae(a, o), u && u.p && (!s || E[0] & /*$$scope*/
      536870912) && Fl(
        u,
        r,
        d,
        /*$$scope*/
        d[29],
        s ? Il(
          r,
          /*$$scope*/
          d[29],
          E,
          Ho
        ) : Dl(
          /*$$scope*/
          d[29]
        ),
        Vn
      );
    },
    i(d) {
      s || (pe(t.$$.fragment, d), pe(u, d), s = !0);
    },
    o(d) {
      Se(t.$$.fragment, d), Se(u, d), s = !1;
    },
    d(d) {
      d && (S(e), S(n), S(i), S(f)), Ol(t), u && u.d(d);
    }
  };
}
function Wo(l) {
  let e, t, n, i, o, a, f, s, r, u = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Xn(l)
  );
  function d(h, k) {
    if (
      /*progress*/
      h[7]
    ) return Yo;
    if (
      /*queue_position*/
      h[2] !== null && /*queue_size*/
      h[3] !== void 0 && /*queue_position*/
      h[2] >= 0
    ) return Vo;
    if (
      /*queue_position*/
      h[2] === 0
    ) return qo;
  }
  let E = d(l), g = E && E(l), A = (
    /*timer*/
    l[5] && Qn(l)
  );
  const D = [Ko, Xo], R = [];
  function U(h, k) {
    return (
      /*last_progress_level*/
      h[15] != null ? 0 : (
        /*show_progress*/
        h[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = U(l)) && (a = R[o] = D[o](l));
  let p = !/*timer*/
  l[5] && il(l);
  return {
    c() {
      u && u.c(), e = se(), t = ve("div"), g && g.c(), n = se(), A && A.c(), i = se(), a && a.c(), f = se(), p && p.c(), s = it(), he(t, "class", "progress-text svelte-v0wucf"), oe(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), oe(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(h, k) {
      u && u.m(h, k), L(h, e, k), L(h, t, k), g && g.m(t, null), Ve(t, n), A && A.m(t, null), L(h, i, k), ~o && R[o].m(h, k), L(h, f, k), p && p.m(h, k), L(h, s, k), r = !0;
    },
    p(h, k) {
      /*variant*/
      h[8] === "default" && /*show_eta_bar*/
      h[18] && /*show_progress*/
      h[6] === "full" ? u ? u.p(h, k) : (u = Xn(h), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), E === (E = d(h)) && g ? g.p(h, k) : (g && g.d(1), g = E && E(h), g && (g.c(), g.m(t, n))), /*timer*/
      h[5] ? A ? A.p(h, k) : (A = Qn(h), A.c(), A.m(t, null)) : A && (A.d(1), A = null), (!r || k[0] & /*variant*/
      256) && oe(
        t,
        "meta-text-center",
        /*variant*/
        h[8] === "center"
      ), (!r || k[0] & /*variant*/
      256) && oe(
        t,
        "meta-text",
        /*variant*/
        h[8] === "default"
      );
      let I = o;
      o = U(h), o === I ? ~o && R[o].p(h, k) : (a && (nn(), Se(R[I], 1, 1, () => {
        R[I] = null;
      }), tn()), ~o ? (a = R[o], a ? a.p(h, k) : (a = R[o] = D[o](h), a.c()), pe(a, 1), a.m(f.parentNode, f)) : a = null), /*timer*/
      h[5] ? p && (nn(), Se(p, 1, 1, () => {
        p = null;
      }), tn()) : p ? (p.p(h, k), k[0] & /*timer*/
      32 && pe(p, 1)) : (p = il(h), p.c(), pe(p, 1), p.m(s.parentNode, s));
    },
    i(h) {
      r || (pe(a), pe(p), r = !0);
    },
    o(h) {
      Se(a), Se(p), r = !1;
    },
    d(h) {
      h && (S(e), S(t), S(i), S(f), S(s)), u && u.d(h), g && g.d(), A && A.d(), ~o && R[o].d(h), p && p.d(h);
    }
  };
}
function Xn(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ve("div"), he(e, "class", "eta-bar svelte-v0wucf"), ze(e, "transform", t);
    },
    m(n, i) {
      L(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && ze(e, "transform", t);
    },
    d(n) {
      n && S(e);
    }
  };
}
function qo(l) {
  let e;
  return {
    c() {
      e = V("processing |");
    },
    m(t, n) {
      L(t, e, n);
    },
    p: ln,
    d(t) {
      t && S(e);
    }
  };
}
function Vo(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, o, a;
  return {
    c() {
      e = V("queue: "), n = V(t), i = V("/"), o = V(
        /*queue_size*/
        l[3]
      ), a = V(" |");
    },
    m(f, s) {
      L(f, e, s), L(f, n, s), L(f, i, s), L(f, o, s), L(f, a, s);
    },
    p(f, s) {
      s[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && ae(n, t), s[0] & /*queue_size*/
      8 && ae(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (S(e), S(n), S(i), S(o), S(a));
    }
  };
}
function Yo(l) {
  let e, t = Ut(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Jn(Zn(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = it();
    },
    m(i, o) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, o);
      L(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = Ut(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const f = Zn(i, t, a);
          n[a] ? n[a].p(f, o) : (n[a] = Jn(f), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && S(e), Ml(n, i);
    }
  };
}
function Kn(l) {
  let e, t = (
    /*p*/
    l[41].unit + ""
  ), n, i, o = " ", a;
  function f(u, d) {
    return (
      /*p*/
      u[41].length != null ? Zo : jo
    );
  }
  let s = f(l), r = s(l);
  return {
    c() {
      r.c(), e = se(), n = V(t), i = V(" | "), a = V(o);
    },
    m(u, d) {
      r.m(u, d), L(u, e, d), L(u, n, d), L(u, i, d), L(u, a, d);
    },
    p(u, d) {
      s === (s = f(u)) && r ? r.p(u, d) : (r.d(1), r = s(u), r && (r.c(), r.m(e.parentNode, e))), d[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[41].unit + "") && ae(n, t);
    },
    d(u) {
      u && (S(e), S(n), S(i), S(a)), r.d(u);
    }
  };
}
function jo(l) {
  let e = tt(
    /*p*/
    l[41].index || 0
  ) + "", t;
  return {
    c() {
      t = V(e);
    },
    m(n, i) {
      L(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = tt(
        /*p*/
        n[41].index || 0
      ) + "") && ae(t, e);
    },
    d(n) {
      n && S(t);
    }
  };
}
function Zo(l) {
  let e = tt(
    /*p*/
    l[41].index || 0
  ) + "", t, n, i = tt(
    /*p*/
    l[41].length
  ) + "", o;
  return {
    c() {
      t = V(e), n = V("/"), o = V(i);
    },
    m(a, f) {
      L(a, t, f), L(a, n, f), L(a, o, f);
    },
    p(a, f) {
      f[0] & /*progress*/
      128 && e !== (e = tt(
        /*p*/
        a[41].index || 0
      ) + "") && ae(t, e), f[0] & /*progress*/
      128 && i !== (i = tt(
        /*p*/
        a[41].length
      ) + "") && ae(o, i);
    },
    d(a) {
      a && (S(t), S(n), S(o));
    }
  };
}
function Jn(l) {
  let e, t = (
    /*p*/
    l[41].index != null && Kn(l)
  );
  return {
    c() {
      t && t.c(), e = it();
    },
    m(n, i) {
      t && t.m(n, i), L(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].index != null ? t ? t.p(n, i) : (t = Kn(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && S(e), t && t.d(n);
    }
  };
}
function Qn(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = V(
        /*formatted_timer*/
        l[20]
      ), n = V(t), i = V("s");
    },
    m(o, a) {
      L(o, e, a), L(o, n, a), L(o, i, a);
    },
    p(o, a) {
      a[0] & /*formatted_timer*/
      1048576 && ae(
        e,
        /*formatted_timer*/
        o[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && ae(n, t);
    },
    d(o) {
      o && (S(e), S(n), S(i));
    }
  };
}
function Xo(l) {
  let e, t;
  return e = new Mo({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      Rl(e.$$.fragment);
    },
    m(n, i) {
      Pl(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (pe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Se(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ol(e, n);
    }
  };
}
function Ko(l) {
  let e, t, n, i, o, a = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && xn(l)
  );
  return {
    c() {
      e = ve("div"), t = ve("div"), f && f.c(), n = se(), i = ve("div"), o = ve("div"), he(t, "class", "progress-level-inner svelte-v0wucf"), he(o, "class", "progress-bar svelte-v0wucf"), ze(o, "width", a), he(i, "class", "progress-bar-wrap svelte-v0wucf"), he(e, "class", "progress-level svelte-v0wucf");
    },
    m(s, r) {
      L(s, e, r), Ve(e, t), f && f.m(t, null), Ve(e, n), Ve(e, i), Ve(i, o), l[31](o);
    },
    p(s, r) {
      /*progress*/
      s[7] != null ? f ? f.p(s, r) : (f = xn(s), f.c(), f.m(t, null)) : f && (f.d(1), f = null), r[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      s[15] * 100}%`) && ze(o, "width", a);
    },
    i: ln,
    o: ln,
    d(s) {
      s && S(e), f && f.d(), l[31](null);
    }
  };
}
function xn(l) {
  let e, t = Ut(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = ll(jn(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = it();
    },
    m(i, o) {
      for (let a = 0; a < n.length; a += 1)
        n[a] && n[a].m(i, o);
      L(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = Ut(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const f = jn(i, t, a);
          n[a] ? n[a].p(f, o) : (n[a] = ll(f), n[a].c(), n[a].m(e.parentNode, e));
        }
        for (; a < n.length; a += 1)
          n[a].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && S(e), Ml(n, i);
    }
  };
}
function $n(l) {
  let e, t, n, i, o = (
    /*i*/
    l[43] !== 0 && Jo()
  ), a = (
    /*p*/
    l[41].desc != null && el(l)
  ), f = (
    /*p*/
    l[41].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null && tl()
  ), s = (
    /*progress_level*/
    l[14] != null && nl(l)
  );
  return {
    c() {
      o && o.c(), e = se(), a && a.c(), t = se(), f && f.c(), n = se(), s && s.c(), i = it();
    },
    m(r, u) {
      o && o.m(r, u), L(r, e, u), a && a.m(r, u), L(r, t, u), f && f.m(r, u), L(r, n, u), s && s.m(r, u), L(r, i, u);
    },
    p(r, u) {
      /*p*/
      r[41].desc != null ? a ? a.p(r, u) : (a = el(r), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      r[41].desc != null && /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[43]
      ] != null ? f || (f = tl(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      r[14] != null ? s ? s.p(r, u) : (s = nl(r), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(r) {
      r && (S(e), S(t), S(n), S(i)), o && o.d(r), a && a.d(r), f && f.d(r), s && s.d(r);
    }
  };
}
function Jo(l) {
  let e;
  return {
    c() {
      e = V(" /");
    },
    m(t, n) {
      L(t, e, n);
    },
    d(t) {
      t && S(e);
    }
  };
}
function el(l) {
  let e = (
    /*p*/
    l[41].desc + ""
  ), t;
  return {
    c() {
      t = V(e);
    },
    m(n, i) {
      L(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[41].desc + "") && ae(t, e);
    },
    d(n) {
      n && S(t);
    }
  };
}
function tl(l) {
  let e;
  return {
    c() {
      e = V("-");
    },
    m(t, n) {
      L(t, e, n);
    },
    d(t) {
      t && S(e);
    }
  };
}
function nl(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[43]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = V(e), n = V("%");
    },
    m(i, o) {
      L(i, t, o), L(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && ae(t, e);
    },
    d(i) {
      i && (S(t), S(n));
    }
  };
}
function ll(l) {
  let e, t = (
    /*p*/
    (l[41].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[43]
    ] != null) && $n(l)
  );
  return {
    c() {
      t && t.c(), e = it();
    },
    m(n, i) {
      t && t.m(n, i), L(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[41].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[43]
      ] != null ? t ? t.p(n, i) : (t = $n(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && S(e), t && t.d(n);
    }
  };
}
function il(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), a = Nl(
    o,
    l,
    /*$$scope*/
    l[29],
    Yn
  );
  return {
    c() {
      e = ve("p"), t = V(
        /*loading_text*/
        l[9]
      ), n = se(), a && a.c(), he(e, "class", "loading svelte-v0wucf");
    },
    m(f, s) {
      L(f, e, s), Ve(e, t), L(f, n, s), a && a.m(f, s), i = !0;
    },
    p(f, s) {
      (!i || s[0] & /*loading_text*/
      512) && ae(
        t,
        /*loading_text*/
        f[9]
      ), a && a.p && (!i || s[0] & /*$$scope*/
      536870912) && Fl(
        a,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? Il(
          o,
          /*$$scope*/
          f[29],
          s,
          Bo
        ) : Dl(
          /*$$scope*/
          f[29]
        ),
        Yn
      );
    },
    i(f) {
      i || (pe(a, f), i = !0);
    },
    o(f) {
      Se(a, f), i = !1;
    },
    d(f) {
      f && (S(e), S(n)), a && a.d(f);
    }
  };
}
function Qo(l) {
  let e, t, n, i, o;
  const a = [Wo, Go], f = [];
  function s(r, u) {
    return (
      /*status*/
      r[4] === "pending" ? 0 : (
        /*status*/
        r[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = s(l)) && (n = f[t] = a[t](l)), {
    c() {
      e = ve("div"), n && n.c(), he(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-v0wucf"), oe(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), oe(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), oe(
        e,
        "generating",
        /*status*/
        l[4] === "generating" && /*show_progress*/
        l[6] === "full"
      ), oe(
        e,
        "border",
        /*border*/
        l[12]
      ), ze(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), ze(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(r, u) {
      L(r, e, u), ~t && f[t].m(e, null), l[33](e), o = !0;
    },
    p(r, u) {
      let d = t;
      t = s(r), t === d ? ~t && f[t].p(r, u) : (n && (nn(), Se(f[d], 1, 1, () => {
        f[d] = null;
      }), tn()), ~t ? (n = f[t], n ? n.p(r, u) : (n = f[t] = a[t](r), n.c()), pe(n, 1), n.m(e, null)) : n = null), (!o || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      r[8] + " " + /*show_progress*/
      r[6] + " svelte-v0wucf")) && he(e, "class", i), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && oe(e, "hide", !/*status*/
      r[4] || /*status*/
      r[4] === "complete" || /*show_progress*/
      r[6] === "hidden"), (!o || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && oe(
        e,
        "translucent",
        /*variant*/
        r[8] === "center" && /*status*/
        (r[4] === "pending" || /*status*/
        r[4] === "error") || /*translucent*/
        r[11] || /*show_progress*/
        r[6] === "minimal"
      ), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && oe(
        e,
        "generating",
        /*status*/
        r[4] === "generating" && /*show_progress*/
        r[6] === "full"
      ), (!o || u[0] & /*variant, show_progress, border*/
      4416) && oe(
        e,
        "border",
        /*border*/
        r[12]
      ), u[0] & /*absolute*/
      1024 && ze(
        e,
        "position",
        /*absolute*/
        r[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && ze(
        e,
        "padding",
        /*absolute*/
        r[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(r) {
      o || (pe(n), o = !0);
    },
    o(r) {
      Se(n), o = !1;
    },
    d(r) {
      r && S(e), ~t && f[t].d(), l[33](null);
    }
  };
}
var xo = function(l, e, t, n) {
  function i(o) {
    return o instanceof t ? o : new t(function(a) {
      a(o);
    });
  }
  return new (t || (t = Promise))(function(o, a) {
    function f(u) {
      try {
        r(n.next(u));
      } catch (d) {
        a(d);
      }
    }
    function s(u) {
      try {
        r(n.throw(u));
      } catch (d) {
        a(d);
      }
    }
    function r(u) {
      u.done ? o(u.value) : i(u.value).then(f, s);
    }
    r((n = n.apply(l, e || [])).next());
  });
};
let Ct = [], jt = !1;
function $o(l) {
  return xo(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (Ct.push(e), !jt) jt = !0;
      else return;
      yield Fo(), requestAnimationFrame(() => {
        let n = [0, 0];
        for (let i = 0; i < Ct.length; i++) {
          const a = Ct[i].getBoundingClientRect();
          (i === 0 || a.top + window.scrollY <= n[0]) && (n[0] = a.top + window.scrollY, n[1] = i);
        }
        window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), jt = !1, Ct = [];
      });
    }
  });
}
function es(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e;
  this && this.__awaiter;
  const a = zo();
  let { i18n: f } = e, { eta: s = null } = e, { queue_position: r } = e, { queue_size: u } = e, { status: d } = e, { scroll_to_output: E = !1 } = e, { timer: g = !0 } = e, { show_progress: A = "full" } = e, { message: D = null } = e, { progress: R = null } = e, { variant: U = "default" } = e, { loading_text: p = "Loading..." } = e, { absolute: h = !0 } = e, { translucent: k = !1 } = e, { border: I = !1 } = e, { autoscroll: w } = e, Y, K = !1, H = 0, P = 0, B = null, z = null, Q = 0, F = null, _, O = null, C = !0;
  const ge = () => {
    t(0, s = t(27, B = t(19, q = null))), t(25, H = performance.now()), t(26, P = 0), K = !0, bt();
  };
  function bt() {
    requestAnimationFrame(() => {
      t(26, P = (performance.now() - H) / 1e3), K && bt();
    });
  }
  function ot() {
    t(26, P = 0), t(0, s = t(27, B = t(19, q = null))), K && (K = !1);
  }
  Uo(() => {
    K && ot();
  });
  let q = null;
  function wt(b) {
    qn[b ? "unshift" : "push"](() => {
      O = b, t(16, O), t(7, R), t(14, F), t(15, _);
    });
  }
  const j = () => {
    a("clear_status");
  };
  function Tt(b) {
    qn[b ? "unshift" : "push"](() => {
      Y = b, t(13, Y);
    });
  }
  return l.$$set = (b) => {
    "i18n" in b && t(1, f = b.i18n), "eta" in b && t(0, s = b.eta), "queue_position" in b && t(2, r = b.queue_position), "queue_size" in b && t(3, u = b.queue_size), "status" in b && t(4, d = b.status), "scroll_to_output" in b && t(22, E = b.scroll_to_output), "timer" in b && t(5, g = b.timer), "show_progress" in b && t(6, A = b.show_progress), "message" in b && t(23, D = b.message), "progress" in b && t(7, R = b.progress), "variant" in b && t(8, U = b.variant), "loading_text" in b && t(9, p = b.loading_text), "absolute" in b && t(10, h = b.absolute), "translucent" in b && t(11, k = b.translucent), "border" in b && t(12, I = b.border), "autoscroll" in b && t(24, w = b.autoscroll), "$$scope" in b && t(29, o = b.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && t(0, s = B), s != null && B !== s && (t(28, z = (performance.now() - H) / 1e3 + s), t(19, q = z.toFixed(1)), t(27, B = s))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, Q = z === null || z <= 0 || !P ? null : Math.min(P / z, 1)), l.$$.dirty[0] & /*progress*/
    128 && R != null && t(18, C = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (R != null ? t(14, F = R.map((b) => {
      if (b.index != null && b.length != null)
        return b.index / b.length;
      if (b.progress != null)
        return b.progress;
    })) : t(14, F = null), F ? (t(15, _ = F[F.length - 1]), O && (_ === 0 ? t(16, O.style.transition = "0", O) : t(16, O.style.transition = "150ms", O))) : t(15, _ = void 0)), l.$$.dirty[0] & /*status*/
    16 && (d === "pending" ? ge() : ot()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && Y && E && (d === "pending" || d === "complete") && $o(Y, w), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = P.toFixed(1));
  }, [
    s,
    f,
    r,
    u,
    d,
    g,
    A,
    R,
    U,
    p,
    h,
    k,
    I,
    Y,
    F,
    _,
    O,
    Q,
    C,
    q,
    n,
    a,
    E,
    D,
    w,
    H,
    P,
    B,
    z,
    o,
    i,
    wt,
    j,
    Tt
  ];
}
class ts extends Do {
  constructor(e) {
    super(), Io(
      this,
      e,
      es,
      Qo,
      Po,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
/*! @license DOMPurify 3.1.6 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.1.6/LICENSE */
const {
  entries: Ul,
  setPrototypeOf: ol,
  isFrozen: ns,
  getPrototypeOf: ls,
  getOwnPropertyDescriptor: is
} = Object;
let {
  freeze: ee,
  seal: re,
  create: zl
} = Object, {
  apply: on,
  construct: sn
} = typeof Reflect < "u" && Reflect;
ee || (ee = function(e) {
  return e;
});
re || (re = function(e) {
  return e;
});
on || (on = function(e, t, n) {
  return e.apply(t, n);
});
sn || (sn = function(e, t) {
  return new e(...t);
});
const Rt = ie(Array.prototype.forEach), sl = ie(Array.prototype.pop), ut = ie(Array.prototype.push), Ft = ie(String.prototype.toLowerCase), Zt = ie(String.prototype.toString), al = ie(String.prototype.match), _t = ie(String.prototype.replace), os = ie(String.prototype.indexOf), ss = ie(String.prototype.trim), me = ie(Object.prototype.hasOwnProperty), $ = ie(RegExp.prototype.test), dt = as(TypeError);
function ie(l) {
  return function(e) {
    for (var t = arguments.length, n = new Array(t > 1 ? t - 1 : 0), i = 1; i < t; i++)
      n[i - 1] = arguments[i];
    return on(l, e, n);
  };
}
function as(l) {
  return function() {
    for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
      t[n] = arguments[n];
    return sn(l, t);
  };
}
function N(l, e) {
  let t = arguments.length > 2 && arguments[2] !== void 0 ? arguments[2] : Ft;
  ol && ol(l, null);
  let n = e.length;
  for (; n--; ) {
    let i = e[n];
    if (typeof i == "string") {
      const o = t(i);
      o !== i && (ns(e) || (e[n] = o), i = o);
    }
    l[i] = !0;
  }
  return l;
}
function rs(l) {
  for (let e = 0; e < l.length; e++)
    me(l, e) || (l[e] = null);
  return l;
}
function qe(l) {
  const e = zl(null);
  for (const [t, n] of Ul(l))
    me(l, t) && (Array.isArray(n) ? e[t] = rs(n) : n && typeof n == "object" && n.constructor === Object ? e[t] = qe(n) : e[t] = n);
  return e;
}
function mt(l, e) {
  for (; l !== null; ) {
    const n = is(l, e);
    if (n) {
      if (n.get)
        return ie(n.get);
      if (typeof n.value == "function")
        return ie(n.value);
    }
    l = ls(l);
  }
  function t() {
    return null;
  }
  return t;
}
const rl = ee(["a", "abbr", "acronym", "address", "area", "article", "aside", "audio", "b", "bdi", "bdo", "big", "blink", "blockquote", "body", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "content", "data", "datalist", "dd", "decorator", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt", "element", "em", "fieldset", "figcaption", "figure", "font", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "img", "input", "ins", "kbd", "label", "legend", "li", "main", "map", "mark", "marquee", "menu", "menuitem", "meter", "nav", "nobr", "ol", "optgroup", "option", "output", "p", "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "section", "select", "shadow", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]), Xt = ee(["svg", "a", "altglyph", "altglyphdef", "altglyphitem", "animatecolor", "animatemotion", "animatetransform", "circle", "clippath", "defs", "desc", "ellipse", "filter", "font", "g", "glyph", "glyphref", "hkern", "image", "line", "lineargradient", "marker", "mask", "metadata", "mpath", "path", "pattern", "polygon", "polyline", "radialgradient", "rect", "stop", "style", "switch", "symbol", "text", "textpath", "title", "tref", "tspan", "view", "vkern"]), Kt = ee(["feBlend", "feColorMatrix", "feComponentTransfer", "feComposite", "feConvolveMatrix", "feDiffuseLighting", "feDisplacementMap", "feDistantLight", "feDropShadow", "feFlood", "feFuncA", "feFuncB", "feFuncG", "feFuncR", "feGaussianBlur", "feImage", "feMerge", "feMergeNode", "feMorphology", "feOffset", "fePointLight", "feSpecularLighting", "feSpotLight", "feTile", "feTurbulence"]), fs = ee(["animate", "color-profile", "cursor", "discard", "font-face", "font-face-format", "font-face-name", "font-face-src", "font-face-uri", "foreignobject", "hatch", "hatchpath", "mesh", "meshgradient", "meshpatch", "meshrow", "missing-glyph", "script", "set", "solidcolor", "unknown", "use"]), Jt = ee(["math", "menclose", "merror", "mfenced", "mfrac", "mglyph", "mi", "mlabeledtr", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow", "ms", "mspace", "msqrt", "mstyle", "msub", "msup", "msubsup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "mprescripts"]), cs = ee(["maction", "maligngroup", "malignmark", "mlongdiv", "mscarries", "mscarry", "msgroup", "mstack", "msline", "msrow", "semantics", "annotation", "annotation-xml", "mprescripts", "none"]), fl = ee(["#text"]), cl = ee(["accept", "action", "align", "alt", "autocapitalize", "autocomplete", "autopictureinpicture", "autoplay", "background", "bgcolor", "border", "capture", "cellpadding", "cellspacing", "checked", "cite", "class", "clear", "color", "cols", "colspan", "controls", "controlslist", "coords", "crossorigin", "datetime", "decoding", "default", "dir", "disabled", "disablepictureinpicture", "disableremoteplayback", "download", "draggable", "enctype", "enterkeyhint", "face", "for", "headers", "height", "hidden", "high", "href", "hreflang", "id", "inputmode", "integrity", "ismap", "kind", "label", "lang", "list", "loading", "loop", "low", "max", "maxlength", "media", "method", "min", "minlength", "multiple", "muted", "name", "nonce", "noshade", "novalidate", "nowrap", "open", "optimum", "pattern", "placeholder", "playsinline", "popover", "popovertarget", "popovertargetaction", "poster", "preload", "pubdate", "radiogroup", "readonly", "rel", "required", "rev", "reversed", "role", "rows", "rowspan", "spellcheck", "scope", "selected", "shape", "size", "sizes", "span", "srclang", "start", "src", "srcset", "step", "style", "summary", "tabindex", "title", "translate", "type", "usemap", "valign", "value", "width", "wrap", "xmlns", "slot"]), Qt = ee(["accent-height", "accumulate", "additive", "alignment-baseline", "ascent", "attributename", "attributetype", "azimuth", "basefrequency", "baseline-shift", "begin", "bias", "by", "class", "clip", "clippathunits", "clip-path", "clip-rule", "color", "color-interpolation", "color-interpolation-filters", "color-profile", "color-rendering", "cx", "cy", "d", "dx", "dy", "diffuseconstant", "direction", "display", "divisor", "dur", "edgemode", "elevation", "end", "fill", "fill-opacity", "fill-rule", "filter", "filterunits", "flood-color", "flood-opacity", "font-family", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-variant", "font-weight", "fx", "fy", "g1", "g2", "glyph-name", "glyphref", "gradientunits", "gradienttransform", "height", "href", "id", "image-rendering", "in", "in2", "k", "k1", "k2", "k3", "k4", "kerning", "keypoints", "keysplines", "keytimes", "lang", "lengthadjust", "letter-spacing", "kernelmatrix", "kernelunitlength", "lighting-color", "local", "marker-end", "marker-mid", "marker-start", "markerheight", "markerunits", "markerwidth", "maskcontentunits", "maskunits", "max", "mask", "media", "method", "mode", "min", "name", "numoctaves", "offset", "operator", "opacity", "order", "orient", "orientation", "origin", "overflow", "paint-order", "path", "pathlength", "patterncontentunits", "patterntransform", "patternunits", "points", "preservealpha", "preserveaspectratio", "primitiveunits", "r", "rx", "ry", "radius", "refx", "refy", "repeatcount", "repeatdur", "restart", "result", "rotate", "scale", "seed", "shape-rendering", "specularconstant", "specularexponent", "spreadmethod", "startoffset", "stddeviation", "stitchtiles", "stop-color", "stop-opacity", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke", "stroke-width", "style", "surfacescale", "systemlanguage", "tabindex", "targetx", "targety", "transform", "transform-origin", "text-anchor", "text-decoration", "text-rendering", "textlength", "type", "u1", "u2", "unicode", "values", "viewbox", "visibility", "version", "vert-adv-y", "vert-origin-x", "vert-origin-y", "width", "word-spacing", "wrap", "writing-mode", "xchannelselector", "ychannelselector", "x", "x1", "x2", "xmlns", "y", "y1", "y2", "z", "zoomandpan"]), ul = ee(["accent", "accentunder", "align", "bevelled", "close", "columnsalign", "columnlines", "columnspan", "denomalign", "depth", "dir", "display", "displaystyle", "encoding", "fence", "frame", "height", "href", "id", "largeop", "length", "linethickness", "lspace", "lquote", "mathbackground", "mathcolor", "mathsize", "mathvariant", "maxsize", "minsize", "movablelimits", "notation", "numalign", "open", "rowalign", "rowlines", "rowspacing", "rowspan", "rspace", "rquote", "scriptlevel", "scriptminsize", "scriptsizemultiplier", "selection", "separator", "separators", "stretchy", "subscriptshift", "supscriptshift", "symmetric", "voffset", "width", "xmlns"]), Nt = ee(["xlink:href", "xml:id", "xlink:title", "xml:space", "xmlns:xlink"]), us = re(/\{\{[\w\W]*|[\w\W]*\}\}/gm), _s = re(/<%[\w\W]*|[\w\W]*%>/gm), ds = re(/\${[\w\W]*}/gm), ms = re(/^data-[\-\w.\u00B7-\uFFFF]/), ps = re(/^aria-[\-\w]+$/), Hl = re(
  /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  // eslint-disable-line no-useless-escape
), hs = re(/^(?:\w+script|data):/i), gs = re(
  /[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g
  // eslint-disable-line no-control-regex
), Bl = re(/^html$/i), bs = re(/^[a-z][.\w]*(-[.\w]+)+$/i);
var _l = /* @__PURE__ */ Object.freeze({
  __proto__: null,
  MUSTACHE_EXPR: us,
  ERB_EXPR: _s,
  TMPLIT_EXPR: ds,
  DATA_ATTR: ms,
  ARIA_ATTR: ps,
  IS_ALLOWED_URI: Hl,
  IS_SCRIPT_OR_DATA: hs,
  ATTR_WHITESPACE: gs,
  DOCTYPE_NAME: Bl,
  CUSTOM_ELEMENT: bs
});
const pt = {
  element: 1,
  attribute: 2,
  text: 3,
  cdataSection: 4,
  entityReference: 5,
  // Deprecated
  entityNode: 6,
  // Deprecated
  progressingInstruction: 7,
  comment: 8,
  document: 9,
  documentType: 10,
  documentFragment: 11,
  notation: 12
  // Deprecated
}, ws = function() {
  return typeof window > "u" ? null : window;
}, Ts = function(e, t) {
  if (typeof e != "object" || typeof e.createPolicy != "function")
    return null;
  let n = null;
  const i = "data-tt-policy-suffix";
  t && t.hasAttribute(i) && (n = t.getAttribute(i));
  const o = "dompurify" + (n ? "#" + n : "");
  try {
    return e.createPolicy(o, {
      createHTML(a) {
        return a;
      },
      createScriptURL(a) {
        return a;
      }
    });
  } catch {
    return console.warn("TrustedTypes policy " + o + " could not be created."), null;
  }
};
function Gl() {
  let l = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : ws();
  const e = (y) => Gl(y);
  if (e.version = "3.1.6", e.removed = [], !l || !l.document || l.document.nodeType !== pt.document)
    return e.isSupported = !1, e;
  let {
    document: t
  } = l;
  const n = t, i = n.currentScript, {
    DocumentFragment: o,
    HTMLTemplateElement: a,
    Node: f,
    Element: s,
    NodeFilter: r,
    NamedNodeMap: u = l.NamedNodeMap || l.MozNamedAttrMap,
    HTMLFormElement: d,
    DOMParser: E,
    trustedTypes: g
  } = l, A = s.prototype, D = mt(A, "cloneNode"), R = mt(A, "remove"), U = mt(A, "nextSibling"), p = mt(A, "childNodes"), h = mt(A, "parentNode");
  if (typeof a == "function") {
    const y = t.createElement("template");
    y.content && y.content.ownerDocument && (t = y.content.ownerDocument);
  }
  let k, I = "";
  const {
    implementation: w,
    createNodeIterator: Y,
    createDocumentFragment: K,
    getElementsByTagName: H
  } = t, {
    importNode: P
  } = n;
  let B = {};
  e.isSupported = typeof Ul == "function" && typeof h == "function" && w && w.createHTMLDocument !== void 0;
  const {
    MUSTACHE_EXPR: z,
    ERB_EXPR: Q,
    TMPLIT_EXPR: F,
    DATA_ATTR: _,
    ARIA_ATTR: O,
    IS_SCRIPT_OR_DATA: C,
    ATTR_WHITESPACE: ge,
    CUSTOM_ELEMENT: bt
  } = _l;
  let {
    IS_ALLOWED_URI: ot
  } = _l, q = null;
  const wt = N({}, [...rl, ...Xt, ...Kt, ...Jt, ...fl]);
  let j = null;
  const Tt = N({}, [...cl, ...Qt, ...ul, ...Nt]);
  let b = Object.seal(zl(null, {
    tagNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    attributeNameCheck: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: null
    },
    allowCustomizedBuiltInElements: {
      writable: !0,
      configurable: !1,
      enumerable: !0,
      value: !1
    }
  })), He = null, Me = null, Be = !0, st = !0, De = !1, Ge = !0, Ie = !1, at = !0, fe = !1, ce = !1, We = !1, Ze = !1, Et = !1, yt = !1, un = !0, _n = !1;
  const Wl = "user-content-";
  let Ht = !0, rt = !1, Xe = {}, Ke = null;
  const dn = N({}, ["annotation-xml", "audio", "colgroup", "desc", "foreignobject", "head", "iframe", "math", "mi", "mn", "mo", "ms", "mtext", "noembed", "noframes", "noscript", "plaintext", "script", "style", "svg", "template", "thead", "title", "video", "xmp"]);
  let mn = null;
  const pn = N({}, ["audio", "video", "img", "source", "image", "track"]);
  let Bt = null;
  const hn = N({}, ["alt", "class", "for", "id", "label", "name", "pattern", "placeholder", "role", "summary", "title", "value", "style", "xmlns"]), At = "http://www.w3.org/1998/Math/MathML", kt = "http://www.w3.org/2000/svg", Ce = "http://www.w3.org/1999/xhtml";
  let Je = Ce, Gt = !1, Wt = null;
  const ql = N({}, [At, kt, Ce], Zt);
  let ft = null;
  const Vl = ["application/xhtml+xml", "text/html"], Yl = "text/html";
  let Z = null, Qe = null;
  const jl = t.createElement("form"), gn = function(c) {
    return c instanceof RegExp || c instanceof Function;
  }, qt = function() {
    let c = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    if (!(Qe && Qe === c)) {
      if ((!c || typeof c != "object") && (c = {}), c = qe(c), ft = // eslint-disable-next-line unicorn/prefer-includes
      Vl.indexOf(c.PARSER_MEDIA_TYPE) === -1 ? Yl : c.PARSER_MEDIA_TYPE, Z = ft === "application/xhtml+xml" ? Zt : Ft, q = me(c, "ALLOWED_TAGS") ? N({}, c.ALLOWED_TAGS, Z) : wt, j = me(c, "ALLOWED_ATTR") ? N({}, c.ALLOWED_ATTR, Z) : Tt, Wt = me(c, "ALLOWED_NAMESPACES") ? N({}, c.ALLOWED_NAMESPACES, Zt) : ql, Bt = me(c, "ADD_URI_SAFE_ATTR") ? N(
        qe(hn),
        // eslint-disable-line indent
        c.ADD_URI_SAFE_ATTR,
        // eslint-disable-line indent
        Z
        // eslint-disable-line indent
      ) : hn, mn = me(c, "ADD_DATA_URI_TAGS") ? N(
        qe(pn),
        // eslint-disable-line indent
        c.ADD_DATA_URI_TAGS,
        // eslint-disable-line indent
        Z
        // eslint-disable-line indent
      ) : pn, Ke = me(c, "FORBID_CONTENTS") ? N({}, c.FORBID_CONTENTS, Z) : dn, He = me(c, "FORBID_TAGS") ? N({}, c.FORBID_TAGS, Z) : {}, Me = me(c, "FORBID_ATTR") ? N({}, c.FORBID_ATTR, Z) : {}, Xe = me(c, "USE_PROFILES") ? c.USE_PROFILES : !1, Be = c.ALLOW_ARIA_ATTR !== !1, st = c.ALLOW_DATA_ATTR !== !1, De = c.ALLOW_UNKNOWN_PROTOCOLS || !1, Ge = c.ALLOW_SELF_CLOSE_IN_ATTR !== !1, Ie = c.SAFE_FOR_TEMPLATES || !1, at = c.SAFE_FOR_XML !== !1, fe = c.WHOLE_DOCUMENT || !1, Ze = c.RETURN_DOM || !1, Et = c.RETURN_DOM_FRAGMENT || !1, yt = c.RETURN_TRUSTED_TYPE || !1, We = c.FORCE_BODY || !1, un = c.SANITIZE_DOM !== !1, _n = c.SANITIZE_NAMED_PROPS || !1, Ht = c.KEEP_CONTENT !== !1, rt = c.IN_PLACE || !1, ot = c.ALLOWED_URI_REGEXP || Hl, Je = c.NAMESPACE || Ce, b = c.CUSTOM_ELEMENT_HANDLING || {}, c.CUSTOM_ELEMENT_HANDLING && gn(c.CUSTOM_ELEMENT_HANDLING.tagNameCheck) && (b.tagNameCheck = c.CUSTOM_ELEMENT_HANDLING.tagNameCheck), c.CUSTOM_ELEMENT_HANDLING && gn(c.CUSTOM_ELEMENT_HANDLING.attributeNameCheck) && (b.attributeNameCheck = c.CUSTOM_ELEMENT_HANDLING.attributeNameCheck), c.CUSTOM_ELEMENT_HANDLING && typeof c.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements == "boolean" && (b.allowCustomizedBuiltInElements = c.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements), Ie && (st = !1), Et && (Ze = !0), Xe && (q = N({}, fl), j = [], Xe.html === !0 && (N(q, rl), N(j, cl)), Xe.svg === !0 && (N(q, Xt), N(j, Qt), N(j, Nt)), Xe.svgFilters === !0 && (N(q, Kt), N(j, Qt), N(j, Nt)), Xe.mathMl === !0 && (N(q, Jt), N(j, ul), N(j, Nt))), c.ADD_TAGS && (q === wt && (q = qe(q)), N(q, c.ADD_TAGS, Z)), c.ADD_ATTR && (j === Tt && (j = qe(j)), N(j, c.ADD_ATTR, Z)), c.ADD_URI_SAFE_ATTR && N(Bt, c.ADD_URI_SAFE_ATTR, Z), c.FORBID_CONTENTS && (Ke === dn && (Ke = qe(Ke)), N(Ke, c.FORBID_CONTENTS, Z)), Ht && (q["#text"] = !0), fe && N(q, ["html", "head", "body"]), q.table && (N(q, ["tbody"]), delete He.tbody), c.TRUSTED_TYPES_POLICY) {
        if (typeof c.TRUSTED_TYPES_POLICY.createHTML != "function")
          throw dt('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');
        if (typeof c.TRUSTED_TYPES_POLICY.createScriptURL != "function")
          throw dt('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');
        k = c.TRUSTED_TYPES_POLICY, I = k.createHTML("");
      } else
        k === void 0 && (k = Ts(g, i)), k !== null && typeof I == "string" && (I = k.createHTML(""));
      ee && ee(c), Qe = c;
    }
  }, bn = N({}, ["mi", "mo", "mn", "ms", "mtext"]), wn = N({}, ["foreignobject", "annotation-xml"]), Zl = N({}, ["title", "style", "font", "a", "script"]), Tn = N({}, [...Xt, ...Kt, ...fs]), En = N({}, [...Jt, ...cs]), Xl = function(c) {
    let m = h(c);
    (!m || !m.tagName) && (m = {
      namespaceURI: Je,
      tagName: "template"
    });
    const T = Ft(c.tagName), G = Ft(m.tagName);
    return Wt[c.namespaceURI] ? c.namespaceURI === kt ? m.namespaceURI === Ce ? T === "svg" : m.namespaceURI === At ? T === "svg" && (G === "annotation-xml" || bn[G]) : !!Tn[T] : c.namespaceURI === At ? m.namespaceURI === Ce ? T === "math" : m.namespaceURI === kt ? T === "math" && wn[G] : !!En[T] : c.namespaceURI === Ce ? m.namespaceURI === kt && !wn[G] || m.namespaceURI === At && !bn[G] ? !1 : !En[T] && (Zl[T] || !Tn[T]) : !!(ft === "application/xhtml+xml" && Wt[c.namespaceURI]) : !1;
  }, be = function(c) {
    ut(e.removed, {
      element: c
    });
    try {
      h(c).removeChild(c);
    } catch {
      R(c);
    }
  }, vt = function(c, m) {
    try {
      ut(e.removed, {
        attribute: m.getAttributeNode(c),
        from: m
      });
    } catch {
      ut(e.removed, {
        attribute: null,
        from: m
      });
    }
    if (m.removeAttribute(c), c === "is" && !j[c])
      if (Ze || Et)
        try {
          be(m);
        } catch {
        }
      else
        try {
          m.setAttribute(c, "");
        } catch {
        }
  }, yn = function(c) {
    let m = null, T = null;
    if (We)
      c = "<remove></remove>" + c;
    else {
      const X = al(c, /^[\r\n\t ]+/);
      T = X && X[0];
    }
    ft === "application/xhtml+xml" && Je === Ce && (c = '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>' + c + "</body></html>");
    const G = k ? k.createHTML(c) : c;
    if (Je === Ce)
      try {
        m = new E().parseFromString(G, ft);
      } catch {
      }
    if (!m || !m.documentElement) {
      m = w.createDocument(Je, "template", null);
      try {
        m.documentElement.innerHTML = Gt ? I : G;
      } catch {
      }
    }
    const J = m.body || m.documentElement;
    return c && T && J.insertBefore(t.createTextNode(T), J.childNodes[0] || null), Je === Ce ? H.call(m, fe ? "html" : "body")[0] : fe ? m.documentElement : J;
  }, An = function(c) {
    return Y.call(
      c.ownerDocument || c,
      c,
      // eslint-disable-next-line no-bitwise
      r.SHOW_ELEMENT | r.SHOW_COMMENT | r.SHOW_TEXT | r.SHOW_PROCESSING_INSTRUCTION | r.SHOW_CDATA_SECTION,
      null
    );
  }, kn = function(c) {
    return c instanceof d && (typeof c.nodeName != "string" || typeof c.textContent != "string" || typeof c.removeChild != "function" || !(c.attributes instanceof u) || typeof c.removeAttribute != "function" || typeof c.setAttribute != "function" || typeof c.namespaceURI != "string" || typeof c.insertBefore != "function" || typeof c.hasChildNodes != "function");
  }, vn = function(c) {
    return typeof f == "function" && c instanceof f;
  }, Re = function(c, m, T) {
    B[c] && Rt(B[c], (G) => {
      G.call(e, m, T, Qe);
    });
  }, Sn = function(c) {
    let m = null;
    if (Re("beforeSanitizeElements", c, null), kn(c))
      return be(c), !0;
    const T = Z(c.nodeName);
    if (Re("uponSanitizeElement", c, {
      tagName: T,
      allowedTags: q
    }), c.hasChildNodes() && !vn(c.firstElementChild) && $(/<[/\w]/g, c.innerHTML) && $(/<[/\w]/g, c.textContent) || c.nodeType === pt.progressingInstruction || at && c.nodeType === pt.comment && $(/<[/\w]/g, c.data))
      return be(c), !0;
    if (!q[T] || He[T]) {
      if (!He[T] && Cn(T) && (b.tagNameCheck instanceof RegExp && $(b.tagNameCheck, T) || b.tagNameCheck instanceof Function && b.tagNameCheck(T)))
        return !1;
      if (Ht && !Ke[T]) {
        const G = h(c) || c.parentNode, J = p(c) || c.childNodes;
        if (J && G) {
          const X = J.length;
          for (let te = X - 1; te >= 0; --te) {
            const we = D(J[te], !0);
            we.__removalCount = (c.__removalCount || 0) + 1, G.insertBefore(we, U(c));
          }
        }
      }
      return be(c), !0;
    }
    return c instanceof s && !Xl(c) || (T === "noscript" || T === "noembed" || T === "noframes") && $(/<\/no(script|embed|frames)/i, c.innerHTML) ? (be(c), !0) : (Ie && c.nodeType === pt.text && (m = c.textContent, Rt([z, Q, F], (G) => {
      m = _t(m, G, " ");
    }), c.textContent !== m && (ut(e.removed, {
      element: c.cloneNode()
    }), c.textContent = m)), Re("afterSanitizeElements", c, null), !1);
  }, Ln = function(c, m, T) {
    if (un && (m === "id" || m === "name") && (T in t || T in jl))
      return !1;
    if (!(st && !Me[m] && $(_, m))) {
      if (!(Be && $(O, m))) {
        if (!j[m] || Me[m]) {
          if (
            // First condition does a very basic check if a) it's basically a valid custom element tagname AND
            // b) if the tagName passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            // and c) if the attribute name passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.attributeNameCheck
            !(Cn(c) && (b.tagNameCheck instanceof RegExp && $(b.tagNameCheck, c) || b.tagNameCheck instanceof Function && b.tagNameCheck(c)) && (b.attributeNameCheck instanceof RegExp && $(b.attributeNameCheck, m) || b.attributeNameCheck instanceof Function && b.attributeNameCheck(m)) || // Alternative, second condition checks if it's an `is`-attribute, AND
            // the value passes whatever the user has configured for CUSTOM_ELEMENT_HANDLING.tagNameCheck
            m === "is" && b.allowCustomizedBuiltInElements && (b.tagNameCheck instanceof RegExp && $(b.tagNameCheck, T) || b.tagNameCheck instanceof Function && b.tagNameCheck(T)))
          ) return !1;
        } else if (!Bt[m]) {
          if (!$(ot, _t(T, ge, ""))) {
            if (!((m === "src" || m === "xlink:href" || m === "href") && c !== "script" && os(T, "data:") === 0 && mn[c])) {
              if (!(De && !$(C, _t(T, ge, "")))) {
                if (T)
                  return !1;
              }
            }
          }
        }
      }
    }
    return !0;
  }, Cn = function(c) {
    return c !== "annotation-xml" && al(c, bt);
  }, Rn = function(c) {
    Re("beforeSanitizeAttributes", c, null);
    const {
      attributes: m
    } = c;
    if (!m)
      return;
    const T = {
      attrName: "",
      attrValue: "",
      keepAttr: !0,
      allowedAttributes: j
    };
    let G = m.length;
    for (; G--; ) {
      const J = m[G], {
        name: X,
        namespaceURI: te,
        value: we
      } = J, ct = Z(X);
      let x = X === "value" ? we : ss(we);
      if (T.attrName = ct, T.attrValue = x, T.keepAttr = !0, T.forceKeepAttr = void 0, Re("uponSanitizeAttribute", c, T), x = T.attrValue, at && $(/((--!?|])>)|<\/(style|title)/i, x)) {
        vt(X, c);
        continue;
      }
      if (T.forceKeepAttr || (vt(X, c), !T.keepAttr))
        continue;
      if (!Ge && $(/\/>/i, x)) {
        vt(X, c);
        continue;
      }
      Ie && Rt([z, Q, F], (On) => {
        x = _t(x, On, " ");
      });
      const Nn = Z(c.nodeName);
      if (Ln(Nn, ct, x)) {
        if (_n && (ct === "id" || ct === "name") && (vt(X, c), x = Wl + x), k && typeof g == "object" && typeof g.getAttributeType == "function" && !te)
          switch (g.getAttributeType(Nn, ct)) {
            case "TrustedHTML": {
              x = k.createHTML(x);
              break;
            }
            case "TrustedScriptURL": {
              x = k.createScriptURL(x);
              break;
            }
          }
        try {
          te ? c.setAttributeNS(te, X, x) : c.setAttribute(X, x), kn(c) ? be(c) : sl(e.removed);
        } catch {
        }
      }
    }
    Re("afterSanitizeAttributes", c, null);
  }, Kl = function y(c) {
    let m = null;
    const T = An(c);
    for (Re("beforeSanitizeShadowDOM", c, null); m = T.nextNode(); )
      Re("uponSanitizeShadowNode", m, null), !Sn(m) && (m.content instanceof o && y(m.content), Rn(m));
    Re("afterSanitizeShadowDOM", c, null);
  };
  return e.sanitize = function(y) {
    let c = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : {}, m = null, T = null, G = null, J = null;
    if (Gt = !y, Gt && (y = "<!-->"), typeof y != "string" && !vn(y))
      if (typeof y.toString == "function") {
        if (y = y.toString(), typeof y != "string")
          throw dt("dirty is not a string, aborting");
      } else
        throw dt("toString is not a function");
    if (!e.isSupported)
      return y;
    if (ce || qt(c), e.removed = [], typeof y == "string" && (rt = !1), rt) {
      if (y.nodeName) {
        const we = Z(y.nodeName);
        if (!q[we] || He[we])
          throw dt("root node is forbidden and cannot be sanitized in-place");
      }
    } else if (y instanceof f)
      m = yn("<!---->"), T = m.ownerDocument.importNode(y, !0), T.nodeType === pt.element && T.nodeName === "BODY" || T.nodeName === "HTML" ? m = T : m.appendChild(T);
    else {
      if (!Ze && !Ie && !fe && // eslint-disable-next-line unicorn/prefer-includes
      y.indexOf("<") === -1)
        return k && yt ? k.createHTML(y) : y;
      if (m = yn(y), !m)
        return Ze ? null : yt ? I : "";
    }
    m && We && be(m.firstChild);
    const X = An(rt ? y : m);
    for (; G = X.nextNode(); )
      Sn(G) || (G.content instanceof o && Kl(G.content), Rn(G));
    if (rt)
      return y;
    if (Ze) {
      if (Et)
        for (J = K.call(m.ownerDocument); m.firstChild; )
          J.appendChild(m.firstChild);
      else
        J = m;
      return (j.shadowroot || j.shadowrootmode) && (J = P.call(n, J, !0)), J;
    }
    let te = fe ? m.outerHTML : m.innerHTML;
    return fe && q["!doctype"] && m.ownerDocument && m.ownerDocument.doctype && m.ownerDocument.doctype.name && $(Bl, m.ownerDocument.doctype.name) && (te = "<!DOCTYPE " + m.ownerDocument.doctype.name + `>
` + te), Ie && Rt([z, Q, F], (we) => {
      te = _t(te, we, " ");
    }), k && yt ? k.createHTML(te) : te;
  }, e.setConfig = function() {
    let y = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : {};
    qt(y), ce = !0;
  }, e.clearConfig = function() {
    Qe = null, ce = !1;
  }, e.isValidAttribute = function(y, c, m) {
    Qe || qt({});
    const T = Z(y), G = Z(c);
    return Ln(T, G, m);
  }, e.addHook = function(y, c) {
    typeof c == "function" && (B[y] = B[y] || [], ut(B[y], c));
  }, e.removeHook = function(y) {
    if (B[y])
      return sl(B[y]);
  }, e.removeHooks = function(y) {
    B[y] && (B[y] = []);
  }, e.removeAllHooks = function() {
    B = {};
  }, e;
}
Gl();
const {
  SvelteComponent: Es,
  append: W,
  assign: ys,
  attr: v,
  check_outros: dl,
  create_component: an,
  destroy_component: rn,
  destroy_each: ml,
  detach: Fe,
  element: Pe,
  ensure_array_like: Ot,
  flush: ye,
  get_spread_object: As,
  get_spread_update: ks,
  group_outros: pl,
  init: vs,
  insert: Ue,
  listen: je,
  mount_component: fn,
  run_all: cn,
  safe_not_equal: Ss,
  set_data: zt,
  set_style: Le,
  space: Ae,
  svg_element: ke,
  text: gt,
  toggle_class: nt,
  transition_in: Oe,
  transition_out: Ye
} = window.__gradio__svelte__internal;
function hl(l, e, t) {
  const n = l.slice();
  return n[28] = e[t], n[30] = t, n;
}
function gl(l, e, t) {
  const n = l.slice();
  return n[31] = e[t], n[30] = t, n;
}
function bl(l) {
  let e, t;
  const n = [
    { autoscroll: (
      /*gradio*/
      l[0].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      l[0].i18n
    ) },
    /*loading_status*/
    l[8]
  ];
  let i = {};
  for (let o = 0; o < n.length; o += 1)
    i = ys(i, n[o]);
  return e = new ts({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    l[17]
  ), {
    c() {
      an(e.$$.fragment);
    },
    m(o, a) {
      fn(e, o, a), t = !0;
    },
    p(o, a) {
      const f = a[0] & /*gradio, loading_status*/
      257 ? ks(n, [
        a[0] & /*gradio*/
        1 && { autoscroll: (
          /*gradio*/
          o[0].autoscroll
        ) },
        a[0] & /*gradio*/
        1 && { i18n: (
          /*gradio*/
          o[0].i18n
        ) },
        a[0] & /*loading_status*/
        256 && As(
          /*loading_status*/
          o[8]
        )
      ]) : {};
      e.$set(f);
    },
    i(o) {
      t || (Oe(e.$$.fragment, o), t = !0);
    },
    o(o) {
      Ye(e.$$.fragment, o), t = !1;
    },
    d(o) {
      rn(e, o);
    }
  };
}
function wl(l) {
  let e, t;
  return e = new Xi({
    props: {
      show_label: (
        /*show_label*/
        l[5]
      ),
      info: void 0,
      $$slots: { default: [Ls] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      an(e.$$.fragment);
    },
    m(n, i) {
      fn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*show_label*/
      32 && (o.show_label = /*show_label*/
      n[5]), i[0] & /*label*/
      2 | i[1] & /*$$scope*/
      4 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Oe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ye(e.$$.fragment, n), t = !1;
    },
    d(n) {
      rn(e, n);
    }
  };
}
function Ls(l) {
  let e;
  return {
    c() {
      e = gt(
        /*label*/
        l[1]
      );
    },
    m(t, n) {
      Ue(t, e, n);
    },
    p(t, n) {
      n[0] & /*label*/
      2 && zt(
        e,
        /*label*/
        t[1]
      );
    },
    d(t) {
      t && Fe(e);
    }
  };
}
function Tl(l) {
  let e, t, n, i, o = (
    /*directory*/
    l[31] + ""
  ), a, f, s;
  function r() {
    return (
      /*click_handler_1*/
      l[20](
        /*i*/
        l[30]
      )
    );
  }
  function u() {
    return (
      /*keypress_handler_1*/
      l[21](
        /*i*/
        l[30]
      )
    );
  }
  return {
    c() {
      e = Pe("div"), t = ke("svg"), n = ke("path"), i = Ae(), a = gt(o), v(n, "d", "M1.75 1A1.75 1.75 0 0 0 0 2.75v10.5C0 14.216.784 15 1.75 15h12.5A1.75 1.75 0 0 0 16 13.25v-8.5A1.75 1.75 0 0 0 14.25 3H7.5a.25.25 0 0 1-.2-.1l-.9-1.2C6.07 1.26 5.55 1 5 1H1.75Z"), v(n, "class", "svelte-179ly2y"), v(t, "aria-hidden", "true"), v(t, "focusable", "false"), v(t, "role", "img"), v(t, "class", "Octicon-sc-9kayk9-0 fczqEI svelte-179ly2y"), v(t, "viewBox", "0 0 16 16"), v(t, "width", "16"), v(t, "height", "16"), v(t, "fill", "currentColor"), Le(t, "display", "inline-block"), Le(t, "user-select", "none"), Le(t, "vertical-align", "text-bottom"), Le(t, "overflow", "visible"), v(e, "class", "inode_option svelte-179ly2y"), v(e, "role", "button"), v(e, "tabindex", "0");
    },
    m(d, E) {
      Ue(d, e, E), W(e, t), W(t, n), W(e, i), W(e, a), f || (s = [
        je(e, "click", r),
        je(e, "keypress", u)
      ], f = !0);
    },
    p(d, E) {
      l = d, E[0] & /*directories*/
      1024 && o !== (o = /*directory*/
      l[31] + "") && zt(a, o);
    },
    d(d) {
      d && Fe(e), f = !1, cn(s);
    }
  };
}
function El(l) {
  let e, t, n, i, o = (
    /*filename*/
    l[28] + ""
  ), a, f, s, r;
  function u() {
    return (
      /*click_handler_2*/
      l[22](
        /*i*/
        l[30]
      )
    );
  }
  function d() {
    return (
      /*keypress_handler_2*/
      l[23](
        /*i*/
        l[30]
      )
    );
  }
  return {
    c() {
      e = Pe("div"), t = ke("svg"), n = ke("path"), i = Ae(), a = gt(o), f = Ae(), v(n, "d", "M2 1.75C2 .784 2.784 0 3.75 0h6.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v9.586A1.75 1.75 0 0 1 13.25 16h-9.5A1.75 1.75 0 0 1 2 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h9.5a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 9 4.25V1.5Zm6.75.062V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914-.013-.011Z"), v(n, "class", "svelte-179ly2y"), v(t, "aria-hidden", "true"), v(t, "focusable", "false"), v(t, "role", "img"), v(t, "class", "color-fg-muted svelte-179ly2y"), v(t, "viewBox", "0 0 16 16"), v(t, "width", "16"), v(t, "height", "16"), v(t, "fill", "currentColor"), Le(t, "display", "inline-block"), Le(t, "user-select", "none"), Le(t, "vertical-align", "text-bottom"), Le(t, "overflow", "visible"), v(e, "class", "inode_option svelte-179ly2y"), v(e, "role", "button"), v(e, "tabindex", "0"), nt(
        e,
        "selected",
        /*selected_file_idx*/
        l[12] === /*i*/
        l[30]
      );
    },
    m(E, g) {
      Ue(E, e, g), W(e, t), W(t, n), W(e, i), W(e, a), W(e, f), s || (r = [
        je(e, "click", u),
        je(e, "keypress", d)
      ], s = !0);
    },
    p(E, g) {
      l = E, g[0] & /*files*/
      2048 && o !== (o = /*filename*/
      l[28] + "") && zt(a, o), g[0] & /*selected_file_idx*/
      4096 && nt(
        e,
        "selected",
        /*selected_file_idx*/
        l[12] === /*i*/
        l[30]
      );
    },
    d(E) {
      E && Fe(e), s = !1, cn(r);
    }
  };
}
function Cs(l) {
  let e, t, n, i, o, a, f, s, r, u, d, E, g, A, D, R, U, p, h, k, I, w, Y, K, H = (
    /*loading_status*/
    l[8] && bl(l)
  ), P = (
    /*label*/
    l[1] !== void 0 && wl(l)
  ), B = Ot(
    /*directories*/
    l[10]
  ), z = [];
  for (let _ = 0; _ < B.length; _ += 1)
    z[_] = Tl(gl(l, B, _));
  let Q = Ot(
    /*files*/
    l[11]
  ), F = [];
  for (let _ = 0; _ < Q.length; _ += 1)
    F[_] = El(hl(l, Q, _));
  return {
    c() {
      H && H.c(), e = Ae(), P && P.c(), t = Ae(), n = Pe("div"), i = Pe("div"), o = gt(
        /*full_path*/
        l[13]
      ), a = Ae(), f = Pe("button"), s = Pe("div"), r = ke("svg"), u = ke("path"), d = ke("path"), E = Ae(), g = ke("svg"), A = ke("circle"), D = ke("path"), R = gt(`
		Copy path`), U = Ae(), p = Pe("div"), h = Pe("div"), h.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="16" height="16" style="display: inline; fill: white;" class="svelte-179ly2y"><polygon points="0 45, 45 10, 45 80" class="svelte-179ly2y"></polygon><polygon points="40 45, 85 10, 85 80" class="svelte-179ly2y"></polygon></svg>
				Up`, k = Ae();
      for (let _ = 0; _ < z.length; _ += 1)
        z[_].c();
      I = Ae();
      for (let _ = 0; _ < F.length; _ += 1)
        F[_].c();
      v(i, "class", "scroll-hide path_box svelte-179ly2y"), v(u, "class", "path1 svelte-179ly2y"), v(u, "d", "M5.75 4.75H10.25V1.75H5.75V4.75Z"), v(d, "class", "path2 svelte-179ly2y"), v(d, "d", "M3.25 2.88379C2.9511 3.05669 2.75 3.37987 2.75 3.75001V13.25C2.75 13.8023 3.19772 14.25 3.75 14.25H12.25C12.8023 14.25 13.25 13.8023 13.25 13.25V3.75001C13.25 3.37987 13.0489 3.05669 12.75 2.88379"), v(r, "class", "clippy_icon svelte-179ly2y"), v(r, "width", "16"), v(r, "height", "16"), v(r, "viewBox", "0 0 16 16"), nt(
        r,
        "copying",
        /*copying*/
        l[9]
      ), v(A, "cx", "8"), v(A, "cy", "8"), v(A, "r", "8"), Le(A, "fill", "green"), Le(A, "stroke-width", "0"), v(A, "class", "svelte-179ly2y"), v(D, "d", "M13.25 4.75L6 12L2.75 8.75"), v(D, "class", "svelte-179ly2y"), v(g, "class", "check_icon svelte-179ly2y"), v(g, "width", "16"), v(g, "height", "16"), v(g, "viewBox", "0 0 16 16"), nt(
        g,
        "copying",
        /*copying*/
        l[9]
      ), v(s, "class", "svelte-179ly2y"), v(f, "class", "submit_btn lg secondary svelte-cmf5ev svelte-179ly2y"), v(n, "class", "parent svelte-179ly2y"), v(h, "class", "inode_option svelte-179ly2y"), v(h, "role", "button"), v(h, "tabindex", "0"), v(p, "class", "inodes svelte-179ly2y");
    },
    m(_, O) {
      H && H.m(_, O), Ue(_, e, O), P && P.m(_, O), Ue(_, t, O), Ue(_, n, O), W(n, i), W(i, o), W(n, a), W(n, f), W(f, s), W(s, r), W(r, u), W(r, d), W(s, E), W(s, g), W(g, A), W(g, D), W(f, R), Ue(_, U, O), Ue(_, p, O), W(p, h), W(p, k);
      for (let C = 0; C < z.length; C += 1)
        z[C] && z[C].m(p, null);
      W(p, I);
      for (let C = 0; C < F.length; C += 1)
        F[C] && F[C].m(p, null);
      w = !0, Y || (K = [
        je(
          f,
          "click",
          /*copy*/
          l[15]
        ),
        je(
          h,
          "click",
          /*click_handler*/
          l[18]
        ),
        je(
          h,
          "keypress",
          /*keypress_handler*/
          l[19]
        )
      ], Y = !0);
    },
    p(_, O) {
      if (/*loading_status*/
      _[8] ? H ? (H.p(_, O), O[0] & /*loading_status*/
      256 && Oe(H, 1)) : (H = bl(_), H.c(), Oe(H, 1), H.m(e.parentNode, e)) : H && (pl(), Ye(H, 1, 1, () => {
        H = null;
      }), dl()), /*label*/
      _[1] !== void 0 ? P ? (P.p(_, O), O[0] & /*label*/
      2 && Oe(P, 1)) : (P = wl(_), P.c(), Oe(P, 1), P.m(t.parentNode, t)) : P && (pl(), Ye(P, 1, 1, () => {
        P = null;
      }), dl()), (!w || O[0] & /*full_path*/
      8192) && zt(
        o,
        /*full_path*/
        _[13]
      ), (!w || O[0] & /*copying*/
      512) && nt(
        r,
        "copying",
        /*copying*/
        _[9]
      ), (!w || O[0] & /*copying*/
      512) && nt(
        g,
        "copying",
        /*copying*/
        _[9]
      ), O[0] & /*click, directories*/
      17408) {
        B = Ot(
          /*directories*/
          _[10]
        );
        let C;
        for (C = 0; C < B.length; C += 1) {
          const ge = gl(_, B, C);
          z[C] ? z[C].p(ge, O) : (z[C] = Tl(ge), z[C].c(), z[C].m(p, I));
        }
        for (; C < z.length; C += 1)
          z[C].d(1);
        z.length = B.length;
      }
      if (O[0] & /*selected_file_idx, click, files*/
      22528) {
        Q = Ot(
          /*files*/
          _[11]
        );
        let C;
        for (C = 0; C < Q.length; C += 1) {
          const ge = hl(_, Q, C);
          F[C] ? F[C].p(ge, O) : (F[C] = El(ge), F[C].c(), F[C].m(p, null));
        }
        for (; C < F.length; C += 1)
          F[C].d(1);
        F.length = Q.length;
      }
    },
    i(_) {
      w || (Oe(H), Oe(P), w = !0);
    },
    o(_) {
      Ye(H), Ye(P), w = !1;
    },
    d(_) {
      _ && (Fe(e), Fe(t), Fe(n), Fe(U), Fe(p)), H && H.d(_), P && P.d(_), ml(z, _), ml(F, _), Y = !1, cn(K);
    }
  };
}
function Rs(l) {
  let e, t;
  return e = new ui({
    props: {
      visible: (
        /*visible*/
        l[4]
      ),
      elem_id: (
        /*elem_id*/
        l[2]
      ),
      elem_classes: (
        /*elem_classes*/
        l[3]
      ),
      scale: (
        /*scale*/
        l[6]
      ),
      min_width: (
        /*min_width*/
        l[7]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [Cs] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      an(e.$$.fragment);
    },
    m(n, i) {
      fn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      16 && (o.visible = /*visible*/
      n[4]), i[0] & /*elem_id*/
      4 && (o.elem_id = /*elem_id*/
      n[2]), i[0] & /*elem_classes*/
      8 && (o.elem_classes = /*elem_classes*/
      n[3]), i[0] & /*scale*/
      64 && (o.scale = /*scale*/
      n[6]), i[0] & /*min_width*/
      128 && (o.min_width = /*min_width*/
      n[7]), i[0] & /*files, selected_file_idx, directories, copying, full_path, show_label, label, gradio, loading_status*/
      16163 | i[1] & /*$$scope*/
      4 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Oe(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ye(e.$$.fragment, n), t = !1;
    },
    d(n) {
      rn(e, n);
    }
  };
}
function Ns(l, e, t) {
  let { gradio: n } = e, { label: i = void 0 } = e, { elem_id: o = "" } = e, { elem_classes: a = [] } = e, { visible: f = !0 } = e, { value: s = "" } = e, { show_label: r } = e, { scale: u = null } = e, { min_width: d = void 0 } = e, { loading_status: E = void 0 } = e, g = !1, A = "", D = [], R = [], U = "/", p = -1, h = A;
  function k() {
    let _ = JSON.parse(s);
    _.status == "download" && (A = _.current_path, t(10, D = _.directories), t(11, R = _.files), U = _.separator, Y());
  }
  function I(_, O) {
    if (O === "dict") {
      let C = {
        selected_inode: _ === -1 ? -1 : D[_],
        current_path: A,
        status: "upload"
      };
      t(16, s = JSON.stringify(C)), t(12, p = -1), n.dispatch("change");
    } else O === "file" && (p === _ ? t(12, p = -1) : t(12, p = _), Y());
  }
  function w() {
    navigator.clipboard.writeText(h), g || (t(9, g = !0), setTimeout(
      () => {
        g && t(9, g = !1);
      },
      1e3
    ));
  }
  function Y() {
    let _ = A;
    p != -1 && (_ = _ + U + R[p]), t(13, h = _);
  }
  const K = () => n.dispatch("clear_status", E), H = () => I(-1, "dict"), P = () => I(-1, "dict"), B = (_) => I(_, "dict"), z = (_) => I(_, "dict"), Q = (_) => I(_, "file"), F = (_) => I(_, "file");
  return l.$$set = (_) => {
    "gradio" in _ && t(0, n = _.gradio), "label" in _ && t(1, i = _.label), "elem_id" in _ && t(2, o = _.elem_id), "elem_classes" in _ && t(3, a = _.elem_classes), "visible" in _ && t(4, f = _.visible), "value" in _ && t(16, s = _.value), "show_label" in _ && t(5, r = _.show_label), "scale" in _ && t(6, u = _.scale), "min_width" in _ && t(7, d = _.min_width), "loading_status" in _ && t(8, E = _.loading_status);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*value*/
    65536 && s === null && t(16, s = ""), l.$$.dirty[0] & /*value*/
    65536 && k();
  }, [
    n,
    i,
    o,
    a,
    f,
    r,
    u,
    d,
    E,
    g,
    D,
    R,
    p,
    h,
    I,
    w,
    s,
    K,
    H,
    P,
    B,
    z,
    Q,
    F
  ];
}
class Os extends Es {
  constructor(e) {
    super(), vs(
      this,
      e,
      Ns,
      Rs,
      Ss,
      {
        gradio: 0,
        label: 1,
        elem_id: 2,
        elem_classes: 3,
        visible: 4,
        value: 16,
        show_label: 5,
        scale: 6,
        min_width: 7,
        loading_status: 8
      },
      null,
      [-1, -1]
    );
  }
  get gradio() {
    return this.$$.ctx[0];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), ye();
  }
  get label() {
    return this.$$.ctx[1];
  }
  set label(e) {
    this.$$set({ label: e }), ye();
  }
  get elem_id() {
    return this.$$.ctx[2];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), ye();
  }
  get elem_classes() {
    return this.$$.ctx[3];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), ye();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({ visible: e }), ye();
  }
  get value() {
    return this.$$.ctx[16];
  }
  set value(e) {
    this.$$set({ value: e }), ye();
  }
  get show_label() {
    return this.$$.ctx[5];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), ye();
  }
  get scale() {
    return this.$$.ctx[6];
  }
  set scale(e) {
    this.$$set({ scale: e }), ye();
  }
  get min_width() {
    return this.$$.ctx[7];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), ye();
  }
  get loading_status() {
    return this.$$.ctx[8];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), ye();
  }
}
export {
  Os as default
};
