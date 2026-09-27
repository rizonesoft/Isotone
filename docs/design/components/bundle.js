/* Photon Interface preview helpers. One classic script: window.Photon.
   Icons are the suite's single family (Lucide geometry, ISC license): 24 viewBox, stroke 1.5, round caps and joins, no fills. */
(function () {
  var P = {
    'x': 'M18 6 6 18|m6 6 12 12',
    'check': 'M20 6 9 17l-5-5',
    'minus': 'M5 12h14',
    'plus': 'M5 12h14|M12 5v14',
    'chevron-down': 'm6 9 6 6 6-6',
    'chevron-up': 'm18 15-6-6-6 6',
    'chevron-right': 'm9 18 6-6-6-6',
    'chevron-left': 'm15 18-6-6 6-6',
    'chevrons-right': 'm6 17 5-5-5-5|m13 17 5-5-5-5',
    'chevrons-left': 'm11 17-5-5 5-5|m18 17-5-5 5-5',
    'ellipsis': 'M5 12h.01|M12 12h.01|M19 12h.01',
    'menu': 'M4 6h16|M4 12h16|M4 18h16',
    'pointer': 'M4.04 4.69a.5.5 0 0 1 .65-.65l16 6.5a.5.5 0 0 1-.06.95l-6.12 1.58a2 2 0 0 0-1.44 1.44l-1.58 6.12a.5.5 0 0 1-.95.06z',
    'move': 'M12 2v20|m15 19-3 3-3-3|m19 9 3 3-3 3|M2 12h20|m5 9-3 3 3 3|m9 5 3-3 3 3',
    'marquee': 'M5 3a2 2 0 0 0-2 2|M19 3a2 2 0 0 1 2 2|M21 19a2 2 0 0 1-2 2|M5 21a2 2 0 0 1-2-2|M9 3h1|M9 21h1|M14 3h1|M14 21h1|M3 9v1|M21 9v1|M3 14v1|M21 14v1',
    'lasso': 'M7 22a5 5 0 0 1-2-4|M3.3 14A6.8 6.8 0 0 1 2 10c0-4.4 4.5-8 10-8s10 3.6 10 8-4.5 8-10 8a12 12 0 0 1-5-1|C5 16 2',
    'wand': 'm21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72|m14 7 3 3|M5 6v4|M19 14v4|M10 2v2|M7 8H3|M21 16h-4|M11 3H9',
    'crop': 'M6 2v14a2 2 0 0 0 2 2h14|M18 22V8a2 2 0 0 0-2-2H2',
    'pipette': 'm2 22 1-1h3l9-9|M3 21v-3l9-9|m15 6 3.4-3.4a2.1 2.1 0 1 1 3 3L18 9l.4.4a2.1 2.1 0 1 1-3 3l-3.8-3.8a2.1 2.1 0 1 1 3-3l.4.4Z',
    'brush': 'm9.06 11.9 8.07-8.06a2.85 2.85 0 1 1 4.03 4.03l-8.06 8.08|M7.07 14.94c-1.66 0-3 1.35-3 3.02 0 1.33-2.5 1.52-2 2.02 1.08 1.1 2.49 2.02 4 2.02 2.2 0 4-1.8 4-4.04a3.01 3.01 0 0 0-3-3.02z',
    'eraser': 'm7 21-4.3-4.3c-1-1-1-2.5 0-3.4l9.6-9.6c1-1 2.5-1 3.4 0l5.6 5.6c1 1 1 2.5 0 3.4L13 21|M22 21H7|m5 11 9 9',
    'stamp': 'M5 22h14|M19.27 13.73A2.5 2.5 0 0 0 17.5 13h-11A2.5 2.5 0 0 0 4 15.5V17a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-1.5c0-.66-.26-1.3-.73-1.77Z|M14 13V8.5C14 7 15 7 15 5a3 3 0 0 0-3-3c-1.69 0-3 1-3 3s1 2 1 3.5V13',
    'bucket': 'm19 11-8-8-8.6 8.6a2 2 0 0 0 0 2.8l5.2 5.2c.8.8 2 .8 2.8 0L19 11Z|m5 2 5 5|M2 13h15|M22 20a2 2 0 1 1-4 0c0-1.6 1.7-2.4 2-4 .3 1.6 2 2.4 2 4Z',
    'pen-tool': 'M15.71 21.29a1 1 0 0 1-1.42 0l-1.58-1.58a1 1 0 0 1 0-1.42l5.58-5.58a1 1 0 0 1 1.42 0l1.58 1.58a1 1 0 0 1 0 1.42z|m18 13-1.38-6.87a1 1 0 0 0-.74-.78L3.24 2.03a1 1 0 0 0-1.21 1.21l3.32 12.64a1 1 0 0 0 .78.74L13 18|m2.3 2.3 7.29 7.29|C11 11 2',
    'pencil': 'M21.17 6.81a1 1 0 0 0-3.99-3.99L3.84 16.17a2 2 0 0 0-.5.83l-1.32 4.35a.5.5 0 0 0 .62.62l4.35-1.32a2 2 0 0 0 .83-.5z|m15 5 4 4',
    'type': 'M4 7V4h16v3|M9 20h6|M12 4v16',
    'square': 'R3 3 18 18 2',
    'circle': 'C12 12 10',
    'hand': 'M18 11V6a2 2 0 0 0-4 0|M14 10V4a2 2 0 0 0-4 0v2|M10 10.5V6a2 2 0 0 0-4 0v8|M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15',
    'zoom-in': 'C11 11 8|m21 21-4.3-4.3|M11 8v6|M8 11h6',
    'zoom-out': 'C11 11 8|m21 21-4.3-4.3|M8 11h6',
    'search': 'C11 11 8|m21 21-4.3-4.3',
    'eye': 'M2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 19.88 0 1 1 0 0 1 0 .7 10.75 10.75 0 0 1-19.88 0|C12 12 3',
    'eye-off': 'M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68|M14.08 14.16a3 3 0 0 1-4.24-4.24|M17.48 17.5A10.75 10.75 0 0 1 2.06 12.35a1 1 0 0 1 0-.7 10.75 10.75 0 0 1 4.45-5.14|m2 2 20 20',
    'lock': 'R3 11 18 11 2|M7 11V7a5 5 0 0 1 10 0v4',
    'unlock': 'R3 11 18 11 2|M7 11V7a5 5 0 0 1 9.9-1',
    'link': 'M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71|M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71',
    'layers': 'M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z|m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65|m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65',
    'sliders': 'M21 4h-7|M10 4H3|M21 12h-9|M8 12H3|M21 20h-5|M12 20H3|M14 2v4|M8 10v4|M16 18v4',
    'image': 'R3 3 18 18 2|C9 9 2|m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21',
    'folder': 'M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z',
    'file-plus': 'M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z|M14 2v4a2 2 0 0 0 2 2h4|M9 15h6|M12 18v-6',
    'save': 'M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z|M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7|M7 3v4a1 1 0 0 0 1 1h7',
    'copy': 'R8 8 14 14 2|M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2',
    'restore': 'R3 8 13 13 1|M8 8V4a1 1 0 0 1 1-1h11a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1h-4',
    'trash': 'M3 6h18|M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6|M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2',
    'undo': 'M9 14 4 9l5-5|M4 9h10.5a5.5 5.5 0 0 1 0 11H11',
    'redo': 'm15 14 5-5-5-5|M20 9H9.5a5.5 5.5 0 0 0 0 11H13',
    'rotate': 'M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8|M3 3v5h5',
    'swap': 'M8 3 4 7l4 4|M4 7h16|m16 21 4-4-4-4|M20 17H4',
    'info': 'C12 12 10|M12 16v-4|M12 8h.01',
    'alert': 'm21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3|M12 9v4|M12 17h.01',
    'error': 'C12 12 10|m15 9-6 6|m9 9 6 6',
    'success': 'C12 12 10|m9 12 2 2 4-4',
    'bulb': 'M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5|M9 18h6|M10 22h4',
    'grid': 'R3 3 18 18 2|M3 9h18|M3 15h18|M9 3v18|M15 3v18',
    'magnet': 'm6 15-4-4 6.75-6.77a7.79 7.79 0 0 1 11 11L13 22l-4-4 6.39-6.36a2.14 2.14 0 0 0-3-3L6 15|m5 8 4 4|m12 15 4 4',
    'ruler': 'M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z|m14.5 12.5 2-2|m11.5 9.5 2-2|m8.5 6.5 2-2|m17.5 15.5 2-2',
    'contrast': 'C12 12 10|M12 18a6 6 0 0 0 0-12v12z',
    'mask': 'R3 3 18 18 2|C12 12 5',
    'star': 'M11.53 2.3a.53.53 0 0 1 .95 0l2.31 4.68a2.12 2.12 0 0 0 1.6 1.16l5.16.76a.53.53 0 0 1 .3.9l-3.74 3.64a2.12 2.12 0 0 0-.61 1.88l.88 5.14a.53.53 0 0 1-.77.56l-4.62-2.43a2.12 2.12 0 0 0-1.97 0L6.4 21.01a.53.53 0 0 1-.77-.56l.88-5.14a2.12 2.12 0 0 0-.61-1.88L2.16 9.8a.53.53 0 0 1 .3-.91l5.16-.75a2.12 2.12 0 0 0 1.6-1.16z',
    'flag': 'M4 22V4a1 1 0 0 1 .4-.8A6 6 0 0 1 8 2c3 0 5 2 7.33 2q2 0 3.07-.8A1 1 0 0 1 20 4v10a1 1 0 0 1-.4.8A6 6 0 0 1 16 16c-3 0-5-2-8-2a6 6 0 0 0-4 1.53',
    'camera': 'M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z|C12 13 3',
    'aperture': 'C12 12 10|m14.31 8 5.74 9.94|M9.69 8h11.48|m7.38 12 5.74-9.94|M9.69 16 3.95 6.06|M14.31 16H2.83|m16.62 12-5.74 9.94',
    'fx': 'M4 17c1.5 0 2-1 2.5-3l2-8C9 4 9.5 3 11 3|M4.5 9h6|m13 10 6 7|m19 10-6 7',
    'folder-plus': 'M12 10v6|M9 13h6|M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z',
    'maximize': 'R4 4 16 16 1',
    'external': 'M15 3h6v6|M10 14 21 3|M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6'
  };
  function el(d) {
    if (d.charAt(0) === 'C') { var c = d.slice(1).trim().split(' '); return '<circle cx="' + c[0] + '" cy="' + c[1] + '" r="' + c[2] + '"/>'; }
    if (d.charAt(0) === 'R') { var r = d.slice(1).trim().split(' '); return '<rect x="' + r[0] + '" y="' + r[1] + '" width="' + r[2] + '" height="' + r[3] + '" rx="' + r[4] + '"/>'; }
    return '<path d="' + d + '"/>';
  }
  function svg(name, size, stroke, cls) {
    var def = P[name]; if (!def) return '';
    size = size || 16;
    return '<svg class="ph-i' + (cls ? ' ' + cls : '') + '" viewBox="0 0 24 24" width="' + size + '" height="' + size + '" stroke-width="' + (stroke || 1.5) + '" aria-hidden="true" focusable="false">' + def.split('|').map(el).join('') + '<' + '/svg>';
  }
  function hydrate(root) {
    var list = (root || document).querySelectorAll('i[data-i]');
    for (var i = 0; i < list.length; i++) {
      var n = list[i];
      n.outerHTML = svg(n.getAttribute('data-i'), +(n.getAttribute('data-s') || 16), n.getAttribute('data-w'), n.getAttribute('data-c'));
    }
    wireScrub(root || document);
  }
  // CompactNumberBox scrub label: drag horizontally on the label to change the value (1 per px, Shift x10, Alt x0.1).
  function wireScrub(root) {
    var labels = root.querySelectorAll('[data-scrub]');
    for (var i = 0; i < labels.length; i++) (function (lab) {
      var box = lab.closest('.ph-num'); if (!box) return;
      var input = box.querySelector('input'); if (!input) return;
      lab.addEventListener('pointerdown', function (e) {
        var start = e.clientX, v0 = parseFloat(input.value) || 0;
        var min = parseFloat(input.getAttribute('data-min')), max = parseFloat(input.getAttribute('data-max'));
        lab.setPointerCapture(e.pointerId); box.classList.add('is-scrubbing');
        function move(ev) {
          var step = ev.shiftKey ? 10 : ev.altKey ? 0.1 : 1;
          var v = v0 + Math.round(ev.clientX - start) * step;
          if (!isNaN(min)) v = Math.max(min, v); if (!isNaN(max)) v = Math.min(max, v);
          input.value = step < 1 ? v.toFixed(1) : String(Math.round(v));
        }
        function up() { box.classList.remove('is-scrubbing'); lab.removeEventListener('pointermove', move); lab.removeEventListener('pointerup', up); }
        lab.addEventListener('pointermove', move); lab.addEventListener('pointerup', up);
      });
    })(labels[i]);
  }
  window.Photon = { icons: Object.keys(P), svg: svg, hydrate: hydrate };
})();
