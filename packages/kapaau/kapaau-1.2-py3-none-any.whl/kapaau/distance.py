using System;
using System.Text;
using System.Windows.Forms;
using Script.Methods;
public partial class UserScript:ScriptMethods,IProcessMethods
{
    //the count of process
	//执行次数计数
    int processCount ;  
    float AB_jl,AC_jl,AD_jl,BC_jl,BD_jl,CD_jl;
    string A_result,B_result,C_result,D_result,TCP_result;

    /// <summary>
    /// Initialize the field's value when compiling
	/// 预编译时变量初始化
    /// </summary>
    public void Init()
    {
        //You can add other global fields here
		//变量初始化，其余变量可在该函数中添加
        processCount = 0;
        AB_jl=0;AC_jl=0;AD_jl=0;BC_jl=0;BD_jl=0;CD_jl=0;
        A_result=null;B_result=null;C_result=null;D_result=null;TCP_result=null;
    }

    /// <summary>
    /// Enter the process function when running code once
	/// 流程执行一次进入Process函数
    /// </summary>
    /// <returns></returns>
    public bool Process()
    {
        //You can add your codes here, for realizing your desired function
		//每次执行将进入该函数，此处添加所需的逻辑流程处理
        //MessageBox.Show("Process Success");
        AB_jl=AB;AC_jl=AC;AD_jl=AD;BC_jl=BC;BD_jl=BD;CD_jl=CD;
        TCP_result=TCP;
        if(TCP_result=="A")
        	{
        	A_result="gl";
        	if(AB_jl<800) B_result="gao";
        	else if(AB_jl<1150) B_result="zh";
            else B_result="di";   
        	if(AC_jl<800) C_result="gao";
        	else if(AC_jl<1150) C_result="zh";
            else C_result="di";   
            if(AD_jl<800) D_result="gao";
        	else if(AD_jl<1150) D_result="zh";
            else D_result="di"; 
            }
        else if(TCP_result=="B")
        	{
        	B_result="gl";
        	if(AB_jl<800) A_result="gao";
        	else if(AB_jl<1150) A_result="zh";
            else A_result="di";   
        	if(BC_jl<800) C_result="gao";
        	else if(BC_jl<1150) C_result="zh";
            else C_result="di";   
            if(BD_jl<800) D_result="gao";
        	else if(BD_jl<1150) D_result="zh";
            else D_result="di"; 
            }
         else if(TCP_result=="C")
        	{
        	C_result="gl";
        	if(AC_jl<800) A_result="gao";
        	else if(AC_jl<1150) A_result="zh";
            else A_result="di";   
        	if(BC_jl<800) B_result="gao";
        	else if(BC_jl<1150) B_result="zh";
            else B_result="di";   
            if(CD_jl<800) D_result="gao";
        	else if(CD_jl<1150) D_result="zh";
            else D_result="di"; 
            }
          else if(TCP_result=="D")
        	{
        	D_result="gl";
        	if(AD_jl<800) A_result="gao";
        	else if(AD_jl<1150) A_result="zh";
            else A_result="di";   
        	if(CD_jl<800) C_result="gao";
        	else if(CD_jl<1150) C_result="zh";
            else C_result="di";   
            if(BD_jl<800) B_result="gao";
        	else if(BD_jl<1150) B_result="zh";
            else B_result="di"; 
            }
        A=A_result;
        B=B_result;
		C=C_result;
		D=D_result;       	
        return true;
    }
}
                            