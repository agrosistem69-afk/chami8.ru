/* Comments under an article: Telegram discussion of the channel post about it.
   Post numbers live in /articles/tg-posts.json (the announce workflow adds new ones). */
(function () {
  var box = document.getElementById('comments');
  if (!box) return;
  var slug = location.pathname.replace(/^\/articles\/|\/(index\.html)?$/g, '');
  var channel = 'chami8ru';
  function fallback() {
    box.insertAdjacentHTML('beforeend', '<p class="c-empty">Обсудить статью и задать вопрос можно в нашем Telegram-канале: <a href="https://t.me/' + channel + '" target="_blank" rel="noopener">t.me/' + channel + '</a></p>');
  }
  fetch('/articles/tg-posts.json', { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (map) {
      var id = map[slug];
      if (!id) return fallback();
      var s = document.createElement('script');
      s.async = true;
      s.src = 'https://telegram.org/js/telegram-widget.js?22';
      s.setAttribute('data-telegram-discussion', channel + '/' + id);
      s.setAttribute('data-comments-limit', '10');
      s.setAttribute('data-color', 'A3301C');
      box.appendChild(s);
      box.insertAdjacentHTML('beforeend', '<p class="c-empty">Комментарии через Telegram. <a href="https://t.me/' + channel + '/' + id + '?comment=1" target="_blank" rel="noopener">Открыть обсуждение в Telegram</a></p>');
    })
    .catch(fallback);
})();
