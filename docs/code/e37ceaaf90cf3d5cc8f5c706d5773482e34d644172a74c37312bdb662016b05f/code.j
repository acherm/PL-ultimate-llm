@import <Foundation/Foundation.j>

function main(args)
{
    var name = "World";
    if (args.length > 1)
        name = args[1];

    CPLog.info("Hello, " + name + "!");
}
