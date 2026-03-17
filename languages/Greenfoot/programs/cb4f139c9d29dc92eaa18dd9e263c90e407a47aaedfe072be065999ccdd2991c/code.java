import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

public class Ball  extends Actor{
    private int x;
    private int y;
    private int incx;
    private int incy;

    public Ball(){
        x=350;
        y=250;
        incx=5;
        incy=5;
    }

    @Override
    public void act() {
        int posx = this.getX();
        int posy = this.getY();

        int nuevox = posx + incx;
        int nuevoy = posy + incy;

        this.setLocation(nuevox, nuevoy);

        World mundo = this.getWorld();

        if(nuevox > mundo.getWidth()){
            incx = -incx;
        }

        if(nuevoy > mundo.getHeight()){
           incy = -incy;
           this.setLocation(x, y);
           Greenfoot.delay(100);
        }

        if(nuevoy < 0){
           incy = -incy;
           this.setLocation(x, y);
           Greenfoot.delay(100);
        }

        if(nuevox < 0){
            incx = -incx;
            //posx = x;
           // posy = y;
        }

         if(this.isTouching(Paddle.class)){
            incy = -incy;
        }


    }
}
