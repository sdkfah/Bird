(function() {
    // 1. 在这里输入你量到的原始背景图像素
    const rawPixel = 388;

    // 2. 核心算法转换
    const logicalX = rawPixel / 2; // 处理 2 倍缩放
    const finalPer = logicalX / 272; // 处理阿里 272 逻辑宽度

    const totalTime = 1450 + Math.floor(Math.random() * 200);

    // 3. 构造带随机抖动和变速的人类轨迹证据
    let track = [];
    let steps = 45;
    for (let i = 0; i <= steps; i++) {
        let t = i / steps;
        // Ease-Out-Cubic 曲线模拟自然减速
        let x = Math.floor(logicalX * (1 - Math.pow(1 - t, 3)));
        let y = 15 + (Math.random() > 0.8 ? 1 : 0);
        track.push([x, y, i * Math.floor(totalTime / steps)]);
    }

    // 4. 执行注入
    if (typeof a !== 'undefined' && typeof c !== 'undefined') {
        a.m = track;
        c.per = finalPer;
        c.width = 272;

        if (typeof x !== 'undefined') {
            var encrypted = a.getData();
            x.per = finalPer;
            x.ua = encrypted.ua;
            x.time = totalTime;
            console.log(`[算法执行成功] 原始:${rawPixel}px -> 逻辑:${logicalX}px -> Per:${finalPer.toFixed(4)}`);
        }
    } else {
        console.error("未检测到变量 a 或 c，请确认是否在断点处执行！");
    }
})();