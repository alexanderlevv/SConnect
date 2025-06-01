// Минималистичный JS для управления аудиоплеером (play/pause/перемотка)
// (дополнительно к стандартному audio controls)
// Можно расширить по желанию

document.addEventListener('DOMContentLoaded', function() {
    var audio = document.getElementById('audio');
    if (!audio) return;
    // Пример: кастомные кнопки (если нужны)
    // document.getElementById('play-btn').onclick = function() { audio.play(); };
    // document.getElementById('pause-btn').onclick = function() { audio.pause(); };
    // document.getElementById('seek-btn').onclick = function() { audio.currentTime += 10; };
});
