// 颜色接口
interface Color {
    String getColor();
}

// 红色实现类
class RedColor implements Color {
    @Override
    public String getColor() {
        return "红色";
    }
}

// 绿色实现类
class GreenColor implements Color {
    @Override
    public String getColor() {
        return "绿色";
    }
}

// 笔大小接口
interface PenSize {
    String getSize();
}

// 小笔实现类
class SmallSize implements PenSize {
    @Override
    public String getSize() {
        return "小";
    }
}

// 中笔实现类
class MiddleSize implements PenSize {
    @Override
    public String getSize() {
        return "中";
    }
}

// 大笔实现类
class BigSize implements PenSize {
    @Override
    public String getSize() {
        return "大";
    }
}

// 笔类
class Pen {
    private PenSize size;
    private Color color;
    
    public Pen(PenSize size, Color color) {
        this.size = size;
        this.color = color;
    }
    
    public void draw() {
        System.out.println("使用" + color.getColor() + size.getSize() + "笔绘画");
    }
}

// 测试类
public class PenDemo {
    public static void main(String[] args) {
        // 创建不同类型的画笔并使用
        Pen redSmallPen = new Pen(new SmallSize(), new RedColor());
        redSmallPen.draw();
        
        Pen greenMiddlePen = new Pen(new MiddleSize(), new GreenColor());
        greenMiddlePen.draw();
        
        Pen redBigPen = new Pen(new BigSize(), new RedColor());
        redBigPen.draw();
        
        // 可以很方便地扩展新的组合，例如绿色小笔
        Pen greenSmallPen = new Pen(new SmallSize(), new GreenColor());
        greenSmallPen.draw();
    }
}
