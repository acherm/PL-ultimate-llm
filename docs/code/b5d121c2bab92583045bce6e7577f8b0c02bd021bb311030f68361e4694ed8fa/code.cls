public class MyHelloWorld {

    public static void applyDiscount(Book__c[] books, Decimal quantity, Decimal discount){

        for (Book__c b : books) {

            if (b.price__c * quantity < 1000){

                b.price__c *= (1-(discount/100));

            }

        }

    }

}