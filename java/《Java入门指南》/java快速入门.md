##Java快速入门（很杂）

《Java轻松入门》（人民邮电出版社  郝焕 编著）

1.this是隐性参数，方法调用的时候，尽管方法的参数列表里面没有this，java都会“默默“地将this参数传递给方法。
```java
class Human
{
    int getHeight()
    {
        return this.height;
    }

    int height;
}
```
this并不是必需的，上述方法可以写为：
```java
    int getHeight()
    {
        return height;
    }
```

2.System.out.print()输出不换行，System.out.println()执行一次后自动换行

3.循环中使用标签，用来在内层循环中越层终止外层循环。标签和break联合使用时，break后面的标签名必须是标记的break所属循环或者其外置循环，而不能是不相干的循环。
```java
public class Test 
{

    public static void main(String[] args) 
    {
        //标签只能标记循环代码
        product:
        for(int run = 1; run < 5; run++)
        {
            for(int count = 1; count < 4; count++)
            {
                System.out.println(run + "," + count);
                if(count == 2) break product;
            }
        }
    }
}
```

4.包：从一定意义上说，就是包路径，只不过起始于源代码的根路径，中间以“.”分割，而不是以“\”。包的声明方式：
```package 包名```
通俗点：包的作用就是让每一个源代码文件的全路径都是唯一的，减少重名的麻烦。

使用包中的类：
```
import 类的含包名全路径，如import xxx.Test
使用：Test t = new Test();
```

5.类（狗类）：
```java
class Dog{
    private String color;
    private int age;
    private String name;
    
    public Dog(){
    }
    
    public Dog(String color, int age, String name){
        this.color = color;
        this.age = age;
        this.name = name;
    }
    
    public void bark(){
        System.out.println("汪....");
    }
    
    public String getColor(){
        return color;
    }
    
    public void setAge(int age){
        this.age = age;
    }
}
```

6.static
```java
public class Dog{
    private String color = "黄色";
    private int age = 1;
    private String name = "花花";
    private static int dogsCount;
    private static int dogsDiedCount;
    //用static初始化某些静态数据
    static{
        dogsCount = 0;
        dogsDiedCount = 0;
        System.out.println("到static块了");
    }
    
    public Dog(){
        dogsCount++;
    }
    
    public Dog(String color, int age, String name){
        this.color = color;
        this.age = age;
        this.name = name;
        dogsCount++;
    }
    
    public void bark(){
        System.out.println("汪....");
    }
    
    public String getColor(){
        return color;
    }
    
    public void setAge(int age){
        this.age = age;
    }
    
    public static void main(String[] args){
        System.out.println("现在有 " + Dog.dogsCount + " 只狗生产了");
        System.out.println("现在有 " + Dog.dogsCount + " 只狗死了");
    }
}
```
7.垃圾回收：

1）引用计数：和python类似

2）对象引用遍历：顺藤摸瓜，没人用就惨了。java虚拟机会以固定频率，来中断所有工作，进行一次全面的垃圾回收，之后集中处理，比较适合多线程的机器

8.继承之子类与父类的类型转换
```
总之：一句话，子类就是父类;父类不一定是子类
DogGril gril = new DogGril()
Dog gril = new DogGril()
DogGril gril = new Dog()   这很危险
```
9.继承之后的初始化顺序：
```
创建对象先找类，从子到父全找全
静态内容要共享，找到类时就整完
要问顺序咋安排，先有父来后有子。
把类找齐都存好，先造父来后造子
属性先整后构造，记我口诀不费劲
顺序理清造对象
```
具体点：
```
将父类静态变量初始化
将子类静态变量初始化
将父类的属性初始化
执行父类的构造方法
将子类的属性初始化
执行父类的构造方法
```

10.方法重载与方法的覆写

实现覆写很简单，只需创建一个与父类中希望被进化掉的方法，同名的且同参数列表的方法

父类的方法被覆写后，子类无法通过普通的方法调用父类中的被覆写的方法，若要调用父类被覆写的方法，用super关键字,例如：`super.f()`

静态方法的覆写与成员方法一样，在子类中写一个同名，同参数列表的静态方法

11.抽象类和final类

1）普通的类，都可以用来new出一个对象。但是有一种类，它不能new出对象。它存在的唯一原因就是被继承，声明时需要一个abstract关键字修饰。在抽象类里面，通常会有抽象方法。
```java
/*一个抽象类PosMachine机*/
abstract class PosMachine{
    int amount;
    float unitPrice;
    float discount;
    
    public float caculatePrice(){
        caculateDiscount();
        return amount*unitPrice*discount;
    }
    /*抽象方法没有实现代码，只有方法声明，并且加了abstract作修饰*/
    public abstract void caculateDiscount();
}
```
抽象方法只能存在于抽象类中。事实上，一个类有了抽象方法，那么它必然是一个抽象类。

巧用抽象类：
```java
/*A公司的PosMachine*/
class APosMachine extends PosMachine{
    
    public void caculateDiscount(){
        discount = 0.3f; 
    }
}

/*B公司的PosMachine*/
class BPosMachine extends PosMachine{
    
    public void caculateDiscount(){
        discount = 0.6f; 
    }
}
```
2）不是所有的类都需要继承，被final修饰过，对类意味着不可继承，对方法意味这不可覆写，对方法参数来说，意味着不可在方法体内被重新赋值
```java

/*例如：保证上述的计算总价的方法不能被覆写*/
public final float caculatePrice(){
    caculateDiscount();
    return amount*unitPrice*discount;
}

/*A公司的posmachine不能被继承*/
final class APosMachine extends PosMachine{
    
    public void caculateDiscount(){
        discount = 0.3f; 
    }
}

/*用于参数禁止修改*/
public void testFinal(final PosMachine a){
    /*a = new APosMachine();   因为是final,所以不允许被赋值*/
    a.amount = 5;
}
```
12.接口：面向接口的编程

1）在继承里，知道了java中extends关键字实现继承，是只能继承一个类的。然而如果用接口的implements关键字，是允许一个类实现多个接口的，这也是接口提供一个多重继承机会的原因

事实上，接口更像是一种行为能力的契约，每实现一个接口，就相当于对外界声明了自己拥有一项能力，别的对象可以使用它的这项能力

因此，接口本身的代码里将不会有任何的实现代码，它仅仅是一份对外的声明契约

看一个基于接口编程的实例：
```java
class Human{
    String name;
    String age;
}


interface ShiBaZhang{
    
    public void feiLongZaiTian();
    
    public void kangLongYouHui();
}

class GaiBangHeader extends Human implements ShiBaZhang{
    
    public void feiLongZaiTian(){
        System.out.println("打出飞龙在天！");
    }
    
    public void kangLongYouHui(){
        System.out.println("打出抗龙优惠！");
    }
    

}

public class Main {

    public static void main(String[] args) {
        
        ShiBaZhang guoJing = new GaiBangHeader();
        guoJing.feiLongZaiTian();
        
        ShiBaZhang xiaoFeng = new GaiBangHeader();
        xiaoFeng.kangLongYouHui();
    }

}
```
这种做法就是面向接口编程，特征是：使用者只关心被使用类有没有需要的能力。如果碰到这种场合，使用者只关注某种指定能力，而不关注其它的，建议尽量使用接口来声明对象变量

2）看一个多重“继承”（接口）的实例：
```java
interface ShiBaZhang{
    
    public void feiLongZaiTian();
    
    public void kangLongYouHui();
}


interface DaGouBang{
    
    public void daGou();
}


class GaiBangHeader extends Human implements ShiBaZhang, DaGouBang{
    
    public void feiLongZaiTian(){
        System.out.println("打出飞龙在天！");
    }
    
    public void kangLongYouHui(){
        System.out.println("打出抗龙优惠！");
    }
    
    public void daGou(){
        System.out.println("使用打狗棒法！");
    }

}
```
其实，就是实现多个接口，向世界宣布有很多能力而已

3）接口间的继承
```java
interface ShiBaZhang{
    
    public void feiLongZaiTian();
    
    public void kangLongYouHui();
}

interface ShiBaZhangPlus extends ShiBaZhang{

    int doSomething();
}
```
接口也是可以继承的，但只能是单根继承

12.一切的根java.lang.Object

所有类都有一个最初始的父类Object

1）equals 与 ==

都是用来判断两个对象是否相等，但是有很大区别

2）hashCode方法：返回一个对象的hash code值，就是对象十六进制的内存地址。在没有覆写的equals方法中，判断条件就是两个对象的hash code是否相等，即是否指向同一个对象。所以，推荐覆写了equals方法后，覆写hashCode方法

3）toString方法：一般情况要求程序员对toString方法进行覆写，这个方法用来输出一段描述对象的字符串，通常在debug的时会起到意想不到的巨大作用

实例代码：
```java
class DogDefault{
    String name;
    
    DogDefault(String name){
        this.name = name;
    }
}

class DogOverride{
    String name;
    
    DogOverride(String name){
        this.name = name;
    }
    
    /*覆写equals方法：只要是统一类型且名字相同，就认为相等*/
    public boolean equals(Object obj){
        /*先判断是不是统一类型对象*/
        if (obj instanceof DogOverride){
            return name.equals(((DogOverride)obj).name);
        }
        else return false;
    }
    
    /*覆写toString方法，按自己的意愿来输出对象描述信息*/
    public String toString(){
        String out = "\n本对象的内容为：\n";
        out += ("name 为" + name);
        return out;
    }
}


public class Main{
    public static void main(String[] args){
        /*测试略*/
    }
}
```

13.for循环的一种简单写法：
```java
for(String temp: bag){
    System.out.println("小口袋里的是：" + temp);
}
```
总结一下就是：
```java
for(声明从数组中取出的变量: 数组变量){
    //循环体代码
}
```
14.形形色色的对象仓库

1）有序但容量有限的仓库---数组

2）不限容的大仓库---ArrayList

定义：`ArrayList 对象名 = new ArrayList();`

添加对象到名为test的ArrayList：
```
test.add(xxx)
test.add(i, xxx)         将xxx放入第i+1的位置
```
从ArrayList中获取对象`数据类型 变量名 = (数据类型)ArrayList变量.get(索引位置)`;注意在取出对象时，需要将取出的对象进行转换，否则会出现类型不匹配的错误，一定要进行正确的类型转型

迭代器实现ArrayList的迭代
```java
for(int i = 0; i < ArrayList变量.size(); i++)
{
    .....
}

/*使用迭代器来迭代*/
for(Iterator it = ArrayList.iterator(); it.hasNext();)
{
    temp = (类型转换数据类型)it.next();
    ...
}

for(Object obj: WareHouse){
    ((Dog)obj).bark();
}
```
ArrayList的自定义排序：（以狗狗类为例）
```java
public class Dog implements Comparable{
    private String color = "黄色";
    private int age = 1;
    private String name = "花花";
    private static int dogsCount;
    
    public Dog(){
        dogsCount++;
    }
    
    public Dog(String color, int age, String name){
        this.color = color;
        this.age = age;
        this.name = name;
        dogsCount++;
    }
    
    public void bark(){
        System.out.println("汪....");
    }
    
    public int getAge(){
        return age;
    }
    
    public int compareTo(Object arg0){
        int ret = 1;
        if(arg0 instanceof Dog){
            Dog temp = (Dog)arg0;
            ret = this.age - temp.getAge();
        }
        return ret;
    }
}

/*使用*/
for(Object obj: WareHouse){
    ((Dog)obj).bark();
}

Collections.sort(WareHouse);

for(Object obj: WareHouse){
    ((Dog)obj).bark();
}
```
3）不允许重复的仓库Set

HashSet类：这种实现一般要求放入的元素覆写hashCode方法，除此之外，用法和ArrayList相似

但是，有些区别：

HashSet不允许放入重复元素

HashSet不能借助Collections类进行排序

HashSet方法没有ArrayList丰富
```java
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class SetTest{
    
    public static void main(String[] args){

        Set WareHouse = new HashSet(5);
        /*其余操作和ArrayList相似*/
    }
}
```
TreeSet是Set的另一种实现，HashSet不能进行排序，但是可以利用TreeSet将数据有序输出：
```java
/*在上述代码的基础上：*/
for(Object obj: WareHouse){
    ((Dog)obj).bark();
}
/*排序：*/
TreeSet ts = new TreeSet(WareHouse);
for(Object obj: ts){
    ((Dog)obj).bark();
}
```
TreeSet一般用于将HashSet中的数据顺序输出，提供一种HashSet的另类排序方法

4）易于检索的仓库HashMap

HashMap同样是基于hashCode的一种仓库，有一下特征：

HashMap以键值对的形式存放数据

HashMap中以key的hashCode方法为依据来散列地存放数据

HashMap允许放入空值

HashMap的key是不重复的
```java
Map WareHouse = new HashMap();
/*WareHouse.put(key, value);*/
/*Dog temp = (Dog)WareHouse.get(key);
```
注意，HashMap和HashSet都是基于散列的，所以是不可排序的

HashMap的迭代：
```java
for(Iterator it = WareHouse.values().iterator(); it.hasNext();){
    temp = (Dog)it.next();
    temp.bark();
}
```
15.让仓库更安全：泛型

看看在ArrayList里面是怎么做到的：
```java
List<Dog> dogList = new ArrayList<Dog>();
/*取出时，不再需要转型*/
Dog temp = dogList.get(0);

List<String> strList = new ArrayList<String>();
```















