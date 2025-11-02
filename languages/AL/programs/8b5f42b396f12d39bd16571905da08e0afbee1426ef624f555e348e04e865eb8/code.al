page 50101 Car
{
    PageType = API;
    APIPublisher = 'stefanmaron';
    APIGroup = 'app1';
    APIVersion = 'v2.0';
    EntityName = 'car';
    EntitySetName = 'cars';
    SourceTable = Car;
    DelayedInsert = true;
    ODataKeyFields = SystemId;

    layout
    {
        area(Content)
        {
            repeater(General)
            {
                field(id; Rec.SystemId)
                {
                    ApplicationArea = All;
                    Caption = 'Id';
                    Editable = false;
                }
                field(make; Rec.Make)
                {
                    ApplicationArea = All;
                    Caption = 'Make';
                }
                field(model; Rec.Model)
                {
                    ApplicationArea = All;
                    Caption = 'Model';
                }
                field(year; Rec."Year")
                {
                    ApplicationArea = All;
                    Caption = 'Year';
                }
            }
        }
    }
}