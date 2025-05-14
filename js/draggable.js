// draggable.js - interact.js を用いたドラッグ移動 & 永続化
interact('.widget').draggable({
  inertia: true,
  modifiers: [
    interact.modifiers.restrictRect({
      restriction: 'parent',
      endOnly: true
    })
  ],
  listeners: {
    start(event) {
      const target = event.target;
      target.classList.add('dragging');

      if (!target.dataset.x) {
        const computed = window.getComputedStyle(target);
        target.style.left = computed.left;
        target.style.top = computed.top;
        target.dataset.x = parseFloat(computed.left).toString();
        target.dataset.y = parseFloat(computed.top).toString();
      }
    },
    move (event) {
      const target = event.target;
      const x = (parseFloat(target.dataset.x) || 0) + event.dx;
      const y = (parseFloat(target.dataset.y) || 0) + event.dy;

      target.style.left = `${x}px`;
      target.style.top = `${y}px`;

      target.dataset.x = x.toString();
      target.dataset.y = y.toString();
    },
    end (event) {
      const target = event.target;
      target.classList.remove('dragging');
    }
  }
});


