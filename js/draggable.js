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
    },
    move (event) {
      const target = event.target;

      // ドラッグ開始時の位置を保存
      if (!target.classList.contains('dragged')) {
        target.classList.add('dragged');
        const rect = target.getBoundingClientRect();
        target.style.transform = 'translate(0px, 0px)';
        // 固定位置から絶対位置に変更
        target.style.bottom = '';
        target.style.left = '';
        target.style.top = `${rect.top}px`;
        target.style.left = `${rect.left}px`;
      }

      // 現在の transform 値を取得
      const transform = target.style.transform;
      const matrix = new DOMMatrix(transform);
      const currentX = matrix.m41;
      const currentY = matrix.m42;

      // 新しい位置を計算して適用
      target.style.transform = `translate(${currentX + event.dx}px, ${currentY + event.dy}px)`;
    },
    end (event) {
      const target = event.target;
      target.classList.remove('dragging');
    }
  }
});

// ページロード時にドラッグ状態をリセット
document.addEventListener('DOMContentLoaded', () => {
  const widgets = document.querySelectorAll('.widget');
  widgets.forEach(widget => {
    widget.classList.remove('dragged');
    widget.style.transform = '';
  });
});