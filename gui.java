import JSHOP2.*;
import java.util.*;
import java.lang.reflect.*;

public class gui{
	public static void main(String[] args) {
		ClassLoader classloader = run.class.getClassLoader();
		try {
			Class aClass = classloader.loadClass(args[0]);
			java.lang.reflect.Method method = aClass.getMethod("getPlans");
			LinkedList<Plan> plans = (LinkedList<Plan>) method.invoke(null);
			// System.out.println(plans);
			System.out.println(plans.size()+" plans found!");
			int planIndex = 1;
			for(Plan plan:plans) {
				System.out.println("Plan "+planIndex);
				System.out.println(plan);
				planIndex++;
			}
			// Object o = method.invoke(null);
			// System.out.println(o);
		} catch (Exception e) {
			e.printStackTrace();
		}
		//problem.getPlans();
		new JSHOP2GUI();
	} 
}
