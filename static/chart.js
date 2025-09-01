// 简化的图表绘制库，替代Chart.js
class SimpleChart {
    constructor(ctx, config) {
        this.ctx = ctx;
        this.canvas = ctx.canvas;
        this.config = config;
        this.data = config.data;
        this.options = config.options || {};
        this.draw();
    }

    destroy() {
        // 清空画布
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    // 文本截断方法
    truncateText(ctx, text, maxWidth) {
        const ellipsis = '...';
        let truncated = text;
        
        if (ctx.measureText(text).width <= maxWidth) {
            return text;
        }
        
        // 逐字符减少直到适合宽度
        while (ctx.measureText(truncated + ellipsis).width > maxWidth && truncated.length > 0) {
            truncated = truncated.slice(0, -1);
        }
        
        return truncated + ellipsis;
    }

    draw() {
        const canvas = this.canvas;
        const ctx = this.ctx;
        
        // 设置画布大小
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * window.devicePixelRatio;
        canvas.height = rect.height * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        
        const width = rect.width;
        const height = rect.height;
        
        // 清空画布
        ctx.clearRect(0, 0, width, height);
        
        if (this.config.type === 'bar') {
            this.drawBarChart(width, height);
        }
    }

    drawBarChart(width, height) {
        const ctx = this.ctx;
        const data = this.data;
        const labels = data.labels;
        const values = data.datasets[0].data;
        
        // 动态计算左边距以适应最长的标签
        ctx.font = '12px Arial';
        const maxLabelWidth = Math.max(...labels.map(label => {
            // 如果标签过长，进行截断处理
            const truncatedLabel = this.truncateText(ctx, label, 200);
            return ctx.measureText(truncatedLabel).width;
        }));
        const leftMargin = Math.max(150, maxLabelWidth + 20);
        
        // 设置边距
        const margin = { top: 40, right: 20, bottom: 40, left: leftMargin };
        const chartWidth = width - margin.left - margin.right;
        const chartHeight = height - margin.top - margin.bottom;
        
        // 计算最大值
        const maxValue = Math.max(...values);
        const barHeight = chartHeight / labels.length * 0.8;
        const barSpacing = chartHeight / labels.length * 0.2;
        
        // 绘制标题
        if (this.options.plugins && this.options.plugins.title && this.options.plugins.title.display) {
            ctx.fillStyle = '#333';
            ctx.font = 'bold 16px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(this.options.plugins.title.text, width / 2, 25);
        }
        
        // 绘制条形图
        labels.forEach((label, index) => {
            const value = values[index];
            const barWidth = (value / maxValue) * chartWidth;
            const y = margin.top + index * (barHeight + barSpacing);
            
            // 绘制条形
            ctx.fillStyle = data.datasets[0].backgroundColor || '#3498db';
            ctx.fillRect(margin.left, y, barWidth, barHeight);
            
            // 绘制标签（使用截断后的文本）
            ctx.fillStyle = '#333';
            ctx.font = '12px Arial';
            ctx.textAlign = 'right';
            const truncatedLabel = this.truncateText(ctx, label, margin.left - 20);
            ctx.fillText(truncatedLabel, margin.left - 10, y + barHeight / 2 + 4);
            
            // 绘制数值
            ctx.textAlign = 'left';
            ctx.fillText(value.toFixed(4), margin.left + barWidth + 5, y + barHeight / 2 + 4);
        });
        
        // 绘制X轴标题
        if (this.options.scales && this.options.scales.x && this.options.scales.x.title) {
            ctx.fillStyle = '#666';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(this.options.scales.x.title.text, width / 2, height - 10);
        }
        
        // 绘制Y轴标题
        if (this.options.scales && this.options.scales.y && this.options.scales.y.title) {
            ctx.save();
            ctx.translate(15, height / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillStyle = '#666';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(this.options.scales.y.title.text, 0, 0);
            ctx.restore();
        }
    }
}

// 全局Chart对象，兼容Chart.js API
window.Chart = SimpleChart;

console.log('简化图表库加载成功');