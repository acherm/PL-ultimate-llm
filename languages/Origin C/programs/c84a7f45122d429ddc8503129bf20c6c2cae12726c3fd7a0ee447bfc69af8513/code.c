void new_wks()
{
	Worksheet wks;
	wks.Create("Origin"); // create a Worksheet window with template - Origin

	vector& vecX = wks.Columns(0).GetDataObject();
	vector& vecY = wks.Columns(1).GetDataObject();

	vecX.Data(1, 10, 1);
	vecY.Data(0.1, 1, 0.1);

	vector<string> vsLongName =
	{
		"Index",
		"Data"
	};

	for (int nCol = 0; nCol < wks.GetNumCols(); ++nCol)
	{
		Column col (wks, nCol);
		col.SetLongName(vsLongName[nCol]);
	}
}
