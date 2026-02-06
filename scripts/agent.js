Java.perform(function () {
    var SkuModel = Java.use("cn.damai.commonbusiness.seatbiz.sku.qilin.model.SkuModel");

    // 用于存储上一次发送的数据，防止重复触发
    var lastRawData = "";

    SkuModel["lambda$skuRequest$0"].implementation = function (skuDoloresRequest, specialResultBean) {
        // 1. 获取原始结果字符串
        var rawData = specialResultBean.getResult();

        // 2. 只有当数据发生变化时才发送给 Python
        if (rawData !== null && rawData !== lastRawData) {
            lastRawData = rawData; // 更新缓存

            // 将数据包装发送
            send({
                type: 'SKU_DATA',
                data: rawData
            });

            console.log("[*] 数据已更新，发送至 Python...");
        } else {
            // 如果数据没变，只在控制台打印一个点，不发送 send() 减轻 Python 负担
            console.log("[.] 数据未变化，已过滤");
        }

        // 3. 执行原逻辑
        this["lambda$skuRequest$0"](skuDoloresRequest, specialResultBean);
    };
});