bool solution(string& inputString) {

unordered_map<char, int> charcount;

for (char c: inputString){
    charcount[c]++;
    
}
int oddcount= 0;
 for(const auto& pair : charcount){
     if (pair.second % 2 !=0) {
         oddcount++;
         if (oddcount > 1){
             return false;
         }
     }
 }
 return true;

}
int main(){
    string inputString = "CIVIC";
    if (solution(inputString)){
        cout<<"The String can be rearranged "<<endl;
    }
    else{
        cout<<"The string cannot be rearranged: "<<endl;
    }
    return 0;
}
