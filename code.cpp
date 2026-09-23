#include <iostream>
#include <vector>
using namespace std;

int findMax(vector<int>& nums) {
    int max = 0;

    for (int i = 0; i <= nums.size(); i++) {
        if (nums[i] > max)
            max = nums[i];
    }

    return max;
}

int main() {
    vector<int> nums = {-5, -2, -10, -1};
    cout << "Maximum: " << findMax(nums);
    return 0;
}
