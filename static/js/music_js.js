// 为所有复制按钮添加点击事件
function setupCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async (event) => {
            event.stopPropagation(); // 阻止事件冒泡到列表项（避免触发播放）
            const url = btn.getAttribute('data-url');
            
            try {
                // 现代 Clipboard API
                await navigator.clipboard.writeText(url);
                
                // 视觉反馈
                const originalHTML = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> 已复制';
                btn.classList.add('copied');
                
                // 2秒后恢复原状
                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.classList.remove('copied');
                }, 2000);
                
            } catch (err) {
                console.error('复制失败:', err);
                
                // 兼容旧版浏览器
                try {
                    const textarea = document.createElement('textarea');
                    textarea.value = url;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    
                    alert('链接已复制到剪贴板！');
                } catch (fallbackErr) {
                    alert('复制失败，请手动复制链接');
                }
            }
        });
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    setupCopyButtons();
});

// 如果DOM已经加载完成，直接执行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupCopyButtons);
} else {
    setupCopyButtons();
}

 function copyText() {
       var copyText = document.getElementById("1");
       copyText.select();
       copyText.setSelectionRange(0, 99999);
       navigator.clipboard.writeText(copyText.value).then(function() {
       alert("succeed!");
       }, function(err) {
       alert("failed: " + err);
       });
}

// 域名复制
function copyText(elementId) {
    var copyText = document.getElementById(elementId);
    if (!copyText) {
        alert("要复制的内容未找到！");
        return;
    }

    copyText.select();
    copyText.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(copyText.value).then(function() {
        alert("复制成功！");
    }, function(err) {
        alert("复制出错，请手动选择文本复制： " + err);
    });
}