# 👋 欢迎来到 WisperZ Blogs

**嵌入式 · 工程实践 · 工具链 · 生活碎片**  
一个慢慢积累的角落，留给自己，也留给有缘人。✨

---

<blockquote id="daily-quote" style="font-style: italic; color: #666; border-left: 4px solid #daeb8f; padding-left: 20px; margin: 2em 0; font-size: 1.1em;">
  加载今日名言...
</blockquote>

<script>
  const techQuotes = [
    "编程的艺术就是处理复杂性的艺术。— Edsger Dijkstra（图灵奖得主）",
    "控制复杂性是计算机编程的本质。— Edsger Dijkstra",
    "丑陋的程序和丑陋的吊桥一样容易坍塌。— Eric S. Raymond（开源斗士）",
    "世上只有两种编程语言：一种是总是被人骂的，一种是从来没人用的。— Bjarne Stroustrup（C++之父）",
    "没有银弹（万能药）。— Fred Brooks（《人月神话》作者）",
    "任何傻瓜都能写出计算机能懂的代码，好的程序员能写出人能读懂的代码。— Martin Fowler",
    "Talk is cheap. Show me the code.（话少说，秀代码。）— Linus Torvalds（Linux之父）"
  ];

  function showLocalQuote() {
    const today = new Date().getDate() % techQuotes.length;
    const [quote, author] = techQuotes[today].split('—');
    document.getElementById('daily-quote').innerHTML = `<q>${quote.trim()}</q><br><cite>${author.trim()}</cite>`;
  }

  // 联网获取每日名言
  fetch('https://v1.hitokoto.cn/?c=c')  // c=c 代表“哲理/名言”
    .then(res => res.json())
    .then(data => {
      document.getElementById('daily-quote').innerHTML = 
        `<q>${data.hitokoto}</q><br><cite>— Hitokoto</cite>`;
    })
    .catch(() => {
      // 如果失败，则回退本地名言
      showLocalQuote();
    });
</script>

---

*码农一枚，记录一些代码与日子的交集*